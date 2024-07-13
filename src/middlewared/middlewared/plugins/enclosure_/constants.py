from .model_info import ModelInfo


SYSFS_SLOT_KEY = 'sysfs_slot'
MAPPED_SLOT_KEY = 'mapped_slot'
SUPPORTS_IDENTIFY_KEY = 'supports_identify_light'
MINI_MODEL_BASE = 'MINI'
MINIR_MODEL_BASE = f'{MINI_MODEL_BASE}R'
HEAD_UNIT_DISK_SLOT_START_NUMBER = 1
DISK_FRONT_KEY = 'is_front'
DISK_REAR_KEY = 'is_rear'
DISK_TOP_KEY = 'is_top'
DISK_INTERNAL_KEY = 'is_internal'
MODELS = {
    'F60': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
        'nvme_only': True,
    }),
    'F100': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
        'nvme_only': True,
    }),
    'F130': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
        'nvme_only': True,
    }),
    'H10': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 16,
    }),
    'H20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 16,
    }),
    'M30': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
    }),
    'M40': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
    }),
    'M50': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 28,
        'front_loaded': True,
        'front_slots': 24,
        'rear_slots': 4,
    }),
    'M60': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 28,
        'front_loaded': True,
        'front_slots': 24,
        'rear_slots': 4,
    }),
    'MINI-3.0-E': ModelInfo(**{
        'total_drive_bays': 6,
        'front_loaded': True,
        'front_slots': 6,
    }),
    'MINI-3.0-E+': ModelInfo(**{
        'total_drive_bays': 6,
        'front_loaded': True,
        'front_slots': 6,
    }),
    'MINI-3.0-X': ModelInfo(**{
        'total_drive_bays': 7,
        'front_loaded': True,
        'front_slots': 7,
    }),
    'MINI-3.0-X+': ModelInfo(**{
        'total_drive_bays': 7,
        'front_loaded': True,
        'front_slots': 7,
    }),
    'MINI-3.0-XL+': ModelInfo(**{
        'total_drive_bays': 10,
        'front_loaded': True,
        'front_slots': 10,
    }),
    'MINI-R': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 12,
        'front_loaded': True,
        'front_slots': 12,
    }),
    'R10': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 16,
    }),
    'R20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
    }),
    'R20A': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
    }),
    'R20B': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
    }),
    'R30': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 12,
        'internal_slots': 4,
        'nvme_only': True,
    }),
    'R40': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 48,
        'top_loaded': True,
        'top_slots': 48,
    }),
    'R50': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 51,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 3,
    }),
    'R50B': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 50,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 2,
    }),
    'R50BM': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 52,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 4,
    }),
    'X10': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 12,
        'front_loaded': True,
        'front_slots': 12,
    }),
    'X20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 12,
        'front_loaded': True,
        'front_slots': 12,
    }),
}
