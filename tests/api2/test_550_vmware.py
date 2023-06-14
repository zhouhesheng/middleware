import pytest

from functions import GET, POST, SSH_TEST
from auto_config import ip, user, password, dev_test
# comment pytestmark for development testing with --dev-test
pytestmark = pytest.mark.skipif(dev_test, reason='Skipping for test development testing')
try:
    from config import VMWARE_HOST, VMWARE_USERNAME, VMWARE_PASSWORD
except ImportError:
    pytest.mark.skip(reason='VMware credentials missing in config.py')


def test_01_get_vmware_query():
    results = GET('/vmware/')
    assert results.status_code == 200
    assert isinstance(results.json(), list) is True


def test_02_create_vmware():
    payload = {
        'hostname': VMWARE_HOST,
        'username': VMWARE_USERNAME,
        'password': VMWARE_PASSWORD
    }
    results = POST('/vmware/get_datastores/', payload)
    assert results.status_code == 200, results.text
    assert isinstance(results.json(), list) is True, results.text


def test_03_verify_vmware_get_datastore_do_not_leak_password(request):
    cmd = f"grep -R \"{VMWARE_PASSWORD}\" /var/log/middlewared.log"
    results = SSH_TEST(cmd, user, password, ip)
    assert results['result'] is False, str(results['output'])
