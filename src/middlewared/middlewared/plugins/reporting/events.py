import psutil
import time

from middlewared.event import EventSource
from middlewared.schema import Dict, Float, Int
from middlewared.validators import Range

from .realtime_reporting import get_arc_stats, get_cpu_stats, get_disk_stats, get_interface_stats, get_memory_info


class RealtimeEventSource(EventSource):

    """
    Retrieve real time statistics for CPU, network,
    virtual memory and zfs arc.
    """
    ACCEPTS = Dict(
        Int('interval', default=2, validators=[Range(min_=2)]),
    )
    RETURNS = Dict(
        Dict('cpu', additional_attrs=True),
        Dict(
            'disks',
            Float('busy'),
            Float('read_bytes'),
            Float('write_bytes'),
            Float('read_ops'),
            Float('write_ops'),
        ),
        Dict('interfaces', additional_attrs=True),
        Dict(
            'memory',
            Dict(
                'classes',
                Int('apps'),
                Int('arc'),
                Int('buffers'),
                Int('cache'),
                Int('page_tables'),
                Int('slab_cache'),
                Int('unused'),
            ),
            Dict('extra', additional_attrs=True),
        ),
        Dict('virtual_memory', additional_attrs=True),
        Dict(
            'zfs',
            Int('arc_min_size'),
            Int('arc_max_size'),
            Int('arc_size'),
            Int('arc_metadata_size'),
            Float('cache_hit_ratio'),
        ),
    )

    def run_sync(self):
        interval = self.arg['interval']
        cores = self.middleware.call_sync('system.info')['cores']

        while not self._cancel_sync.is_set():
            # this gathers the most recent metric recorded via netdata (for all charts)
            retries = 2
            while retries > 0:
                try:
                    netdata_metrics = self.middleware.call_sync('netdata.get_all_metrics')
                except Exception:
                    retries -= 1
                    if retries <= 0:
                        raise

                    time.sleep(0.5)
                else:
                    break

            if failed_to_connect := not bool(netdata_metrics):
                data = {'failed_to_connect': failed_to_connect}
            else:
                data = {
                    'zfs': get_arc_stats(),
                    'memory': get_memory_info(netdata_metrics),
                    'virtual_memory': psutil.virtual_memory()._asdict(),
                    'cpu': get_cpu_stats(netdata_metrics, cores),
                    'disks': get_disk_stats(netdata_metrics, self.middleware.call_sync('device.get_disk_names')),
                    'interfaces': get_interface_stats(
                        netdata_metrics, [
                            iface['name'] for iface in self.middleware.call_sync(
                                'interface.query', [], {'extra': {'retrieve_names_only': True}}
                            )
                        ]
                    ),
                    'failed_to_connect': False,
                }

                # CPU temperature
                data['cpu']['temperature_celsius'] = self.middleware.call_sync('reporting.cpu_temperatures') or None

            self.send_event('ADDED', fields=data)
            time.sleep(interval)


def setup(middleware):
    middleware.register_event_source('reporting.realtime', RealtimeEventSource, roles=['REPORTING_READ'])
