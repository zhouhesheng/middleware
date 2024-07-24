import asyncio
from collections import defaultdict

from middlewared.service import (
    CallError, CRUDService, ValidationErrors, filterable, job
)
from middlewared.utils import filter_list

from middlewared.api import api_method
from middlewared.api.current import (
    ContainerEntry,
    ContainerCreateArgs, ContainerCreateResult,
    ContainerUpdateArgs, ContainerUpdateResult,
    ContainerDeleteArgs, ContainerDeleteResult,
    ContainerStateArgs, ContainerStateResult,
)

import aiohttp
import logging


logger = logging.getLogger(__name__)
SOCKET = '/var/lib/incus/unix.socket'
HTTP_URI = 'http://unix.socket/1.0'


class IncusWS(object):

    instance = None

    def __init__(self):
        IncusWS.instance = self
        self._incoming = defaultdict(list)
        self._waiters = defaultdict(list)

    async def run(self):
        while True:
            try:
                await self._run_impl()
            except Exception:
                logger.warning('Incus websocket failure', exc_info=True)
            await asyncio.sleep(1)

    async def _run_impl(self):
        async with aiohttp.UnixConnector(path=SOCKET) as conn:
            async with aiohttp.ClientSession(connector=conn) as session:
                async with session.ws_connect('ws://unix.socket/1.0/events') as ws:
                    async for msg in ws:
                        if msg.type != aiohttp.WSMsgType.TEXT:
                            continue
                        data = msg.json()
                        if data['type'] != 'operation':
                            continue
                        if 'metadata' in data and 'id' in data['metadata']:
                            self._incoming[data['metadata']['id']].append(data)
                            for i in self._waiters[data['metadata']['id']]:
                                i.set()

    async def wait(self, id, callback):
        event = asyncio.Event()
        self._waiters[id].append(event)

        try:
            while True:
                if not self._incoming[id]:
                    await event.wait()
                event.clear()

                for i in list(self._incoming[id]):
                    if await callback(i) is True:
                        return
                    self._incoming[id].remove(i)
        finally:
            self._waiters[id].remove(event)


class ContainerService(CRUDService):

    class Config:
        cli_namespace = 'container'
        entry = ContainerEntry

    @filterable
    async def query(self, filters, options):
        """
        Query all Containers with `query-filters` and `query-options`.
        """
        async with aiohttp.UnixConnector(path=SOCKET) as conn:
            async with aiohttp.ClientSession(connector=conn) as session:
                r = await session.get(f'{HTTP_URI}/instances?filter=&recursion=2')
                results = (await r.json())['metadata']
                for i in results:
                    i['id'] = i['name']
        return filter_list(results, filters, options)

    async def _call_and_wait(self, path, method, request_kwargs=None, running_cb=None):
        async with aiohttp.UnixConnector(path=SOCKET) as conn:
            async with aiohttp.ClientSession(connector=conn) as session:
                methodobj = getattr(session, method)
                r = await methodobj(f'{HTTP_URI}/{path}', **(request_kwargs or {}))
                result = await r.json()

        async def callback(data):
            if data['metadata']['status'] == 'Failure':
                raise CallError(data['metadata']['err'])
            if data['metadata']['status'] == 'Success':
                return True
            if data['metadata']['status'] == 'Running':
                if running_cb:
                    await running_cb(data)

        task = asyncio.ensure_future(IncusWS.instance.wait(result['metadata']['id'], callback))
        try:
            await asyncio.wait_for(task, 300)
        except asyncio.TimeoutError:
            raise CallError('Timed out')

    @api_method(ContainerCreateArgs, ContainerCreateResult)
    @job()
    async def do_create(self, job, data):
        """
        """
        async def running_cb(data):
            if 'metadata' in data['metadata'] and (metadata := data['metadata']['metadata']):
                if 'download_progress' in metadata:
                    job.set_progress(None, metadata['download_progress'])
                if 'create_instance_from_image_unpack_progress' in metadata:
                    job.set_progress(None, metadata['create_instance_from_image_unpack_progress'])

        await self._call_and_wait('instances', 'post', {'json': {
            'name': data['name'],
            'ephemeral': False,
            'source': {
                'type': 'image',
                'server': 'https://images.linuxcontainers.org',
                'protocol': 'simplestreams',
                'mode': 'pull',
                'alias': data['image'],
            },
            'type': 'container',
            'start': True,
        }}, running_cb)

        return await self.middleware.call('container.get_instance', data['name'])

    @api_method(ContainerUpdateArgs, ContainerUpdateResult)
    @job()
    async def do_update(self, job, id, data):
        """
        """
        instance = await self.middleware.call('container.get_instance', id)
        if instance['status'] == 'Running':
            config = instance['config']
            if 'limits_config' in data:
                config['limits.memory'] = data['limits_config']
            await self._call_and_wait(f'instances/{id}', 'put', {'json': instance})

        return await self.middleware.call('container.get_instance', id)

    @api_method(ContainerDeleteArgs, ContainerDeleteResult)
    @job()
    async def do_delete(self, job, id):
        """
        """
        instance = await self.middleware.call('container.get_instance', id)
        if instance['status'] == 'Running':
            await self._call_and_wait(f'instances/{id}/state', 'put', {'json': {
                'action': 'stop',
                'timeout': -1,
                'force': True,
            }})

        await self._call_and_wait(f'instances/{id}', 'delete')

        return True

    @api_method(ContainerStateArgs, ContainerStateResult)
    @job()
    async def state(self, job, id, action, force):
        """
        """
        await self._call_and_wait(f'instances/{id}/state', 'put', {'json': {
            'action': action.lower(),
            'timeout': -1,
            'force': force,
        }})

        return True


async def setup(middleware):
    asyncio.ensure_future(IncusWS().run())
