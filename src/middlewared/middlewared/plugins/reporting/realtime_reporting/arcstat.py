from typing import TypedDict

# The values in this tuple are mostly used to calculate
# ZFS ARC specific memory values. We are essentially
# copying the same logic in the upstream `arc_summary.py`
# script provided by ZFS but pulling out the values we're
# interested in. The reason why we're doing this ourselves
# is, at time of writing, netdata's calculation of similar
# values is wrong. Furthermore, the `arc_summary.py` script
# makes no attempt at explaining these values and so to keep
# things as simple as possible (without confusing the end-user)
# we're going to simplify what we consider "easily understood"
# ZFS ARC memory info without delving into the low-level details.
# The calculated values are used in our reporting.realtime event
# subscription which is primarily consumed by True{Command/Cloud}
# and UI teams.
OTHER_KSTAT_FIELDS = (
    'size',
    'c_max',
    'c_min',
    'pd',
    'pm',
    'meta',
)
KSTAT_CACHE_FIELDS = (
    'anon_data',
    'anon_metadata',
    'mfu_data',
    'mfu_metadata',
    'mru_data',
    'mru_metadata',
    'uncached_data',
    'uncached_metadata',
)
ALL_KSTAT_FIELDS = OTHER_KSTAT_FIELDS + KSTAT_CACHE_FIELDS
_4GiB = 4294967296


class ArcStats(TypedDict):
    arc_min_size: int
    arc_max_size: int
    arc_size: int
    arc_metadata_size: int
    cache_hit_ratio: float  # TODO: wrong, need to remove

    @classmethod
    def create(
        cls,
        arc_min_size: int = 0,
        arc_max_size: int = 0,
        arc_size: int = 0,
        arc_metadata_size: int = 0,
        cache_hit_ratio: float = 0.0,
    ):
        return cls(
            arc_min_size=arc_min_size,
            arc_max_size=arc_max_size,
            arc_size=arc_size,
            arc_metadata_size=arc_metadata_size,
            cache_hit_ratio=cache_hit_ratio
        )


def calculate_arc_stats_impl(arcstats: dict) -> ArcStats:
    if not arcstats:
        return ArcStats.create()

    caches_size = sum([arcstats[i] for i in KSTAT_CACHE_FIELDS])
    c = 0x10000 * caches_size / 0x10000
    mfu_data_target = ((_4GiB - arcstats['pm']) * ((_4GiB - arcstats['meta']) / _4GiB)) / c
    mfu_metadata_target = ((_4GiB - arcstats['pd']) * ((_4GiB - arcstats['meta']) / _4GiB)) / c
    mru_data_target = (arcstats['pd'] * ((_4GiB - arcstats['meta']) / _4GiB)) / c
    mru_metadata_target = (arcstats['pm'] * ((_4GiB - arcstats['meta']) / _4GiB)) / c
    metadata = int(
        arcstats['size'] - sum([
            mfu_data_target, mfu_metadata_target,
            mru_data_target, mru_metadata_target,
        ]) + caches_size
    )

    return ArcStats.create(
        arc_min_size=arcstats['c_min'],
        arc_max_size=arcstats['c_max'],
        arc_size=arcstats['size'],
        arc_metadata_size=metadata,
    )


def get_arc_stats_impl() -> dict[str, int]:
    rv = dict()
    with open('/proc/spl/kstat/zfs/arcstats') as f:
        for lineno, line in filter(lambda x: x[0] > 2, enumerate(f, start=1)):
            try:
                # all failure conditions raise ValueError
                name, _, value = line.strip().split()
                rv[ALL_KSTAT_FIELDS[ALL_KSTAT_FIELDS.index(name.strip())]] = int(value)
            except ValueError:
                continue
    return rv


def get_arc_stats() -> ArcStats:
    return calculate_arc_stats_impl(get_arc_stats_impl())
