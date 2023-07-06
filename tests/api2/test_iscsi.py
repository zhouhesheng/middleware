import contextlib

import sys
import os
sys.path.append(os.getcwd())

import pytest
from pytest_dependency import depends
from middlewared.service_exception import ValidationErrors
from middlewared.test.integration.utils import call
from middlewared.test.integration.assets.pool import dataset
from auto_config import dev_test
# comment pytestmark for development testing with --dev-test
pytestmark = pytest.mark.skipif(dev_test, reason='Skipping for test development testing')


@contextlib.contextmanager
def iscsi_extent(data):
    extent = call("iscsi.extent.create", data)

    try:
        yield extent
    finally:
        call("iscsi.extent.delete", extent["id"])


def test__iscsi_extent__disk_choices(request):
    with dataset("test zvol", {
        "type": "VOLUME",
        "volsize": 1032192,
    }) as ds:
        # Make snapshots available for devices
        call("zfs.dataset.update", ds, {"properties": {"snapdev": {"parsed": "visible"}}})
        call("zfs.snapshot.create", {"dataset": ds, "name": "snap-1"})
        assert call("iscsi.extent.disk_choices") == {
            f'zvol/{ds.replace(" ", "+")}': f'{ds} (1000 KiB)',
            f'zvol/{ds.replace(" ", "+")}@snap-1': f'{ds}@snap-1 [ro]',
        }

        # Create new extent
        with iscsi_extent({
            "name": "test_extent",
            "type": "DISK",
            "disk": f"zvol/{ds.replace(' ', '+')}",
        }):
            # Verify that zvol is not available in iscsi disk choices
            assert call("iscsi.extent.disk_choices") == {
                f'zvol/{ds.replace(" ", "+")}@snap-1': f'{ds}@snap-1 [ro]',
            }
            # Verify that zvol is not availabe in VM disk choices
            # (and snapshot zvol is not available too as it is read-only)
            assert call("vm.device.disk_choices") == {}


def test__iscsi_extent__create_with_invalid_disk_with_whitespace(request):
    with dataset("test zvol", {
        "type": "VOLUME",
        "volsize": 1032192,
    }) as ds:
        with pytest.raises(ValidationErrors) as e:
            with iscsi_extent({
                "name": "test_extent",
                "type": "DISK",
                "disk": f"zvol/{ds}",
            }):
                pass

        assert str(e.value) == (
            f"[EINVAL] iscsi_extent_create.disk: Device '/dev/zvol/{ds}' for volume '{ds}' does not exist\n"
        )


def test__iscsi_extent__locked(request):
    with dataset("test zvol", {
        "type": "VOLUME",
        "volsize": 1032192,
        "inherit_encryption": False,
        "encryption": True,
        "encryption_options": {"passphrase": "testtest"},
    }) as ds:
        with iscsi_extent({
            "name": "test_extent",
            "type": "DISK",
            "disk": f"zvol/{ds.replace(' ', '+')}",
        }) as extent:
            assert not extent["locked"]

            call("pool.dataset.lock", ds, job=True)

            extent = call("iscsi.extent.get_instance", extent["id"])
            assert extent["locked"]
