import pytest
from pytest_dependency import depends

from functions import SSH_TEST
from auto_config import ip, user, password, dev_test
# comment pytestmark for development testing with --dev-test
pytestmark = pytest.mark.skipif(dev_test, reason='Skipping for test development testing')


def test_core_get_methods(request):
    results = SSH_TEST("midclt call core.get_methods", user, password, ip)
    assert results['result'] is True, results
