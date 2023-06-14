import contextlib

from functions import DELETE, POST


@contextlib.contextmanager
def snapshot(dataset_id, snapshot_name):
    payload = {'dataset': dataset_id, 'name': snapshot_name}
    results = POST("/zfs/snapshot/", payload)
    assert results.status_code == 200, results.text
    assert isinstance(results.json(), dict), results.text
    snapshot_config = results.json()

    try:
        yield snapshot_config
    finally:
        snapshot_id = snapshot_config['id'].replace('/', '%2F')
        results = DELETE(f"/zfs/snapshot/id/{snapshot_id}/")
        assert results.status_code == 200, results.text
        assert results.json(), results.text


def snapshot_rollback(snapshot_id):
    results = POST("/zfs/snapshot/rollback", {'id': snapshot_id, 'options': {}})
    assert results.status_code == 200, results.text
