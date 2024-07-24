import aiohttp

from middlewared.service import (
    CallError, CRUDService, ValidationErrors, filterable, job, private
)
from middlewared.utils import filter_list

from middlewared.api import api_method
from middlewared.api.current import (
    VirtInstanceEntry,
    VirtInstancesCreateArgs, VirtInstancesCreateResult,
    VirtInstancesUpdateArgs, VirtInstancesUpdateResult,
    VirtInstancesDeleteArgs, VirtInstancesDeleteResult,
    VirtInstancesStateArgs, VirtInstancesStateResult,
    VirtInstancesImageChoicesArgs, VirtInstancesImageChoicesResult,
    VirtInstancesDeviceListArgs, VirtInstancesDeviceListResult,
    VirtInstancesDeviceAddArgs, VirtInstancesDeviceAddResult,
    VirtInstancesDeviceDeleteArgs, VirtInstancesDeviceDeleteResult,
)
from .utils import incus_call, incus_call_and_wait


IMAGES_SERVER = 'https://images.linuxcontainers.org'
IMAGES_JSON = f'{IMAGES_SERVER}/streams/v1/images.json'


class VirtInstancesService(CRUDService):

    class Config:
        namespace = 'virt.instances'
        cli_namespace = 'virt.instances'
        entry = VirtInstanceEntry
        role_prefix = 'VIRT_INSTANCES'

    @filterable
    async def query(self, filters, options):
        """
        Query all instances with `query-filters` and `query-options`.
        """
        results = (await incus_call('1.0/instances?filter=&recursion=2', 'get'))['metadata']
        entries = []
        for i in results:
            # If entry has no config or state its probably in an unknown state, skip it
            if not i.get('config') or not i.get('state'):
                continue
            entry = {
                'id': i['name'],
                'name': i['name'],
                'type': 'CONTAINER' if i['type'] == 'container' else 'VM',
                'status': i['state']['status'].upper(),
                'cpu': i['config'].get('limits.cpu'),
                'autostart': i['config'].get('boot.autostart') or False,
                'environment': {},
                'raw': i,
            }

            if memory := i['config'].get('limits.memory'):
                # Handle all units? e.g. changes done through CLI
                if memory.endswith('MiB'):
                    memory = int(memory[:-3]) * 1024 * 1024
                else:
                    memory = None
            entry['memory'] = memory

            for k, v in i['config'].items():
                if not k.startswith('environment.'):
                    continue
                entry['environment'][k[12:]] = v
            entries.append(entry)
        return filter_list(entries, filters, options)

    @private
    async def validate(self, new, schema_name, verrors, old=None):
        if not old and await self.query([('name', '=', new['name'])]):
            verrors.add(f'{schema_name}.name', f'Name {new["name"]!r} already exists')

        # Do not validate image_choices because its an expansive operation, just fail on creation

    def __data_to_config(self, data):
        config = {}
        if data.get('environment'):
            for k, v in data['environment'].items():
                config[f'environment.{k}'] = v
        if data.get('cpu'):
            config['limits.cpu'] = data['cpu']

        if data.get('memory'):
            config['limits.memory'] = str(data['memory']) + 'MiB'

        if data.get('autostart') is not None:
            config['boot.autostart'] = str(data['autostart']).lower()
        return config

    @api_method(VirtInstancesImageChoicesArgs, VirtInstancesImageChoicesResult)
    async def image_choices(self):
        """
        Provice choices for instance image from a remote repository.
        """
        choices = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(IMAGES_JSON) as resp:
                data = await resp.json()
                for v in data['products'].values():
                    alias = v['aliases'].split(',', 1)[0]
                    choices[alias] = {
                        'label': f'{v["os"]} {v["release"]} ({v["arch"]}, {v["variant"]})',
                        'os': v['os'],
                        'release': v['release'],
                        'arch': v['arch'],
                        'variant': v['variant'],
                    }
        return choices

    @api_method(VirtInstancesCreateArgs, VirtInstancesCreateResult)
    @job()
    async def do_create(self, job, data):
        """
        Create a new virtualizated instance.
        """

        verrors = ValidationErrors()
        await self.validate(data, 'virt_instance_create', verrors)
        verrors.check()

        async def running_cb(data):
            if 'metadata' in data['metadata'] and (metadata := data['metadata']['metadata']):
                if 'download_progress' in metadata:
                    job.set_progress(None, metadata['download_progress'])
                if 'create_instance_from_image_unpack_progress' in metadata:
                    job.set_progress(None, metadata['create_instance_from_image_unpack_progress'])

        await incus_call_and_wait('1.0/instances', 'post', {'json': {
            'name': data['name'],
            'ephemeral': False,
            'config': self.__data_to_config(data),
            'source': {
                'type': 'image',
                'server': IMAGES_SERVER,
                'protocol': 'simplestreams',
                'mode': 'pull',
                'alias': data['image'],
            },
            'type': 'container' if data['instance_type'] == 'CONTAINER' else 'virtual-machine',
            'start': True,
        }}, running_cb)

        return await self.middleware.call('virt.instances.get_instance', data['name'])

    @api_method(VirtInstancesUpdateArgs, VirtInstancesUpdateResult)
    @job()
    async def do_update(self, job, id, data):
        """
        Update instance.
        """
        instance = await self.middleware.call('virt.instances.get_instance', id)

        verrors = ValidationErrors()
        await self.validate(data, 'virt_instance_create', verrors, old=instance)
        verrors.check()

        instance['raw']['config'].update(self.__data_to_config(data))
        await incus_call_and_wait(f'1.0/instances/{id}', 'put', {'json': instance['raw']})

        return await self.middleware.call('virt.instances.get_instance', id)

    @api_method(VirtInstancesDeleteArgs, VirtInstancesDeleteResult)
    @job()
    async def do_delete(self, job, id):
        """
        Delete an instance.
        """
        instance = await self.middleware.call('virt.instances.get_instance', id)
        if instance['status'] == 'RUNNING':
            await incus_call_and_wait(f'1.0/instances/{id}/state', 'put', {'json': {
                'action': 'stop',
                'timeout': -1,
                'force': True,
            }})

        await incus_call_and_wait(f'1.0/instances/{id}', 'delete')

        return True

    @api_method(VirtInstancesDeviceListArgs, VirtInstancesDeviceListResult, roles=['VIRT_INSTANCES_READ'])
    async def device_list(self, id):
        instance = await self.middleware.call('virt.instances.get_instance', id)
        return instance['raw']['devices']

    @api_method(VirtInstancesDeviceAddArgs, VirtInstancesDeviceAddResult, roles=['VIRT_INSTANCES_WRITE'])
    async def device_add(self, id, device):
        instance = await self.middleware.call('virt.instances.get_instance', id)
        data = instance['raw']

        name = device.pop('name')
        new = {}

        match device['dev_type']:
            case 'DISK':
                new['type'] = 'disk'
                source = device.get('source') or ''
                if not source.startswith(('/dev/zvol/', '/mnt/')):
                    raise CallError('Only pool paths are allowed.')
                new['source'] = device['source']
                if source.startswith('/mnt/'):
                    if not device.get('destination'):
                        raise CallError('Destination is required for filesystem paths.')
                    if instance['type'] == 'VM':
                        raise CallError('Destination is not valid for VM')
                    new['path'] = device['destination']
            case 'USB':
                new['type'] = 'usb'
                new['busnum'] = str(device['bus'])
                new['devnum'] = str(device['dev'])
            case 'TPM':
                new['type'] = 'tpm'
                if device.get('path'):
                    if instance['type'] == 'VM':
                        raise CallError('Path is not valid for VM')
                    new['path'] = device['path']
                elif instance['type'] == 'CONTAINER':
                    raise CallError('Path is required for CONTAINER')

                if device.get('pathrm'):
                    if instance['type'] == 'VM':
                        raise CallError('Pathrm is not valid for VM')
                    new['pathrm'] = device['pathrm']
                elif instance['type'] == 'CONTAINER':
                    raise CallError('Path is required for CONTAINER')
            case _:
                raise Exception('Invalid device type')

        data['devices'][name] = new
        await incus_call_and_wait(f'1.0/instances/{id}', 'put', {'json': data})
        return True

    @api_method(VirtInstancesDeviceDeleteArgs, VirtInstancesDeviceDeleteResult, roles=['VIRT_INSTANCES_DELETE'])
    async def device_delete(self, id, device):
        instance = await self.middleware.call('virt.instances.get_instance', id)
        data = instance['raw']
        data['devices'].pop(device)
        await incus_call_and_wait(f'1.0/instances/{id}', 'put', {'json': data})
        return True

    @api_method(VirtInstancesStateArgs, VirtInstancesStateResult, roles=['VIRT_INSTANCES_WRITE'])
    @job()
    async def state(self, job, id, action, force):
        """
        Change state of an instance.
        """
        await incus_call_and_wait(f'1.0/instances/{id}/state', 'put', {'json': {
            'action': action.lower(),
            'timeout': -1,
            'force': force,
        }})

        return True
