from threading import Event

from middlewared.test.integration.assets.filesystem import mkfile
from middlewared.test.integration.assets.pool import dataset
from middlewared.test.integration.utils.client import client
from middlewared.test.integration.utils.call import call
from middlewared.test.integration.utils.ssh import ssh

from auto_config import pool_name


def clean():
    call('virt.global.update', {'pool': ''}, job=True)
    ssh(f'zfs destroy -r {pool_name}/.ix-virt || true')
    call('virt.global.update', {'pool': 'tank'}, job=True)


def test_virt_instances_create():
    clean()

    wait_agent = Event()

    def wait_debian(*args, **kwargs):
        wait_agent.set()

    with client() as c:
        c.subscribe('virt.instances.agent_running', wait_debian, sync=True)

        # Create first so there is time for the agent to start
        call('virt.instances.create', {'name': 'debian', 'image': 'debian/trixie', 'instance_type': 'VM'}, job=True)

        call('virt.instances.create', {'name': 'void', 'image': 'voidlinux/musl'}, job=True)
        ssh('incus exec void cat /etc/os-release | grep "Void Linux"')

        call('virt.instances.create', {'name': 'arch', 'image': 'archlinux/current/default'}, job=True)
        ssh('incus exec arch cat /etc/os-release | grep "Arch Linux"')

        assert wait_agent.wait(timeout=30)
        ssh('incus exec debian cat /etc/os-release | grep "Debian"')


def test_virt_instances_update():
    call('virt.instances.update', 'void', {'cpu': '1', 'memory': 500, 'environment': {'FOO': 'BAR'}}, job=True)
    ssh('incus exec void grep MemTotal: /proc/meminfo|grep 512000')
    # Checking CPUs seems to cause a racing condition (perhaps CPU currently in use in the container?)
    # rv = ssh('incus exec void cat /proc/cpuinfo |grep processor|wc -l')
    # assert rv.strip() == '1'
    rv = ssh('incus exec void env | grep ^FOO=')
    assert rv.strip() == 'FOO=BAR'


def test_virt_instances_state():
    # Stop only one of them so the others are stopped during delete
    assert ssh('incus list void -f json| jq ".[].status"').strip() == '"Running"'
    call('virt.instances.state', 'void', 'STOP', True, job=True)
    assert ssh('incus list void -f json| jq ".[].status"').strip() == '"Stopped"'


def test_virt_instances_device_add():
    # Stop only one of them so the others are stopped during delete
    assert ssh('incus list debian -f json| jq ".[].status"').strip() == '"Running"'
    call('virt.instances.state', 'debian', 'STOP', True, job=True)

    call('virt.instances.device_add', 'debian', {
        'name': 'tpm',
        'dev_type': 'TPM',
    })

    # TODO: adding to a VM causes start to hang at the moment (zombie process)
    # call('virt.instances.device_add', 'debian', {
    #     'name': 'disk1',
    #     'dev_type': 'DISK',
    #     'source': f'/mnt/{pool_name}',
    #     'destination': '/host',
    # })

    devices = call('virt.instances.device_list', 'debian')
    assert 'tpm' in devices, devices
    # assert 'disk1' in devices, devices

    wait_agent = Event()

    def wait_debian(*args, **kwargs):
        wait_agent.set()

    with client() as c:
        c.subscribe('virt.instances.agent_running', wait_debian, sync=True)
        call('virt.instances.state', 'debian', 'START', False, job=True)
        assert wait_agent.wait(timeout=30)

    ssh('incus exec debian ls /dev/tpm0')
    # ssh('incus exec debian ls /host')

    with dataset('virtshare') as ds:
        call('virt.instances.device_add', 'arch', {
            'name': 'disk1',
            'dev_type': 'DISK',
            'source': f'/mnt/{ds}',
            'destination': '/host',
        })
        devices = call('virt.instances.device_list', 'arch')
        assert 'disk1' in devices, devices
        with mkfile(f'/mnt/{ds}/testfile'):
            ssh('incus exec arch ls /host/testfile')
        call('virt.instances.device_delete', 'arch', 'disk1')


def test_virt_instances_device_delete():
    call('virt.instances.state', 'debian', 'STOP', True, job=True)
    call('virt.instances.device_delete', 'debian', 'tpm')
    devices = call('virt.instances.device_list', 'debian')
    assert 'tpm' not in devices, devices


def test_virt_instances_delete():
    call('virt.instances.delete', 'void', job=True)
    ssh('incus config show void 2>&1 | grep "not found"')

    call('virt.instances.delete', 'arch', job=True)
    ssh('incus config show arch 2>&1 | grep "not found"')

    call('virt.instances.delete', 'debian', job=True)
    ssh('incus config show debian 2>&1 | grep "not found"')

    assert len(call('virt.instances.query')) == 0
