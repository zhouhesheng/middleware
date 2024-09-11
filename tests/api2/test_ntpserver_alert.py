import contextlib
import copy
import time

from middlewared.test.integration.utils import call, ssh

CONFIG_FILE = "/etc/chrony/chrony.conf"
BAD_NTP = "172.16.0.0"


@contextlib.contextmanager
def temp_remove_ntp_config():
    orig = call("system.ntpserver.query")
    try:
        for i in orig:
            _id = i.pop("id")
            assert call("system.ntpserver.delete", _id)
        yield copy.deepcopy(orig[0])  # arbitrarily yield first entry
    finally:
        for i in orig:
            # finally update with original (functional) config
            assert call("system.ntpserver.create", i)


def test_verify_ntp_alert_is_raised():
    with temp_remove_ntp_config() as temp:
        temp["address"] = BAD_NTP
        temp["force"] = True
        temp_id = call("system.ntpserver.create", temp)["id"]
        call("system.ntpserver.query", [["address", "=", BAD_NTP]], {"get": True})

        # verify the OS config
        results = ssh(f'fgrep "{BAD_NTP}" {CONFIG_FILE}', complete_response=True)
        assert results["result"] is True, results

        # verify alert is raised
        max_retries = 10
        for i in range(max_retries):
            alerts = call("alert.run_source", "NTPHealthCheck")
            if alerts and alerts[0]["args"]["reason"].startswith("No Active NTP peers"):
                break
            else:
                time.sleep(1)
        else:
            assert False, f"NO NTP alert after waiting {max_retries} seconds: ALERTS: {alerts!r}"

        # remove our bogus entry
        assert call("system.ntpserver.delete", temp_id)


def test_verify_ntp_alert_is_cleared():
    max_retries = 10
    for i in range(max_retries):
        if len(call("alert.run_source", "NTPHealthCheck")) == 0:
            return
        else:
            max_retries -= 1
            time.sleep(1)

    assert False, f"NTPHealthCheck alert didnt clear after {max_retries} seconds"
