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
T10_VENDORS = {
    'iXsystems': 'iXsystems',
    'AHCI': 'AHCI',
    'BROADCOM': 'BROADCOM',
    'CELESTIC': 'CELESTIC',
    'ECStream': 'ECStream',
    'HGST': 'HGST',
    'iX': 'iX',
    'VikingES': 'VikingES',
}
T10_PRODUCTS = {
    '2024Jp': '2024Jp',
    '2024Js': '2024Js',
    '4024J': '4024J',
    '4024Sp': '4024Sp',
    '4024Ss': '4024Ss',
    '2012Sp': '2012Sp',
    'DSS212Sp': 'DSS212Sp',
    'DSS212Ss': 'DSS212Ss',
    'eDrawer4048S1': 'eDrawer4048S1',
    'eDrawer4048S2': 'eDrawer4048S2',
    'FS1': 'FS1',
    'FS1L': 'FS1L',
    'FS2': 'FS2',
    'H4060-J': 'H4060-J',
    'H4102-J': 'H4102-J',
    'NDS-41022-BB': 'NDS-41022-BB',
    'P3215-O': 'P3215-O',
    'P3217-B': 'P3217-B',
    'R0904-F0001-01': 'R0904-F0001-01',
    'SGPIOEnclosure': 'SGPIOEnclosure',
    'TrueNASSMCSC826-P': 'TrueNASSMCSC826-P',
    'TrueNASR20p': 'TrueNASR20p',
    'VDS-41022-BB': 'VDS-41022-BB',
    'VirtualSES': 'VirtualSES',
    'X2012': 'X2012',
    'X2012-MT': 'X2012-MT',
}
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
        'expected_t10': ('BROADCOM_VirtualSES',),
    }),
    'H20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 16,
        'expected_t10': ('BROADCOM_VirtualSES',),
    }),
    'M30': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
        'expected_t10': (
            'ECStream_4024Sp',
            'ECStream_4024Ss',
            'iX_4024Sp',
            'iX_4024Ss',
        )
    }),
    'M40': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 24,
        'front_loaded': True,
        'front_slots': 24,
        'expected_t10': (
            'ECStream_4024Sp',
            'ECStream_4024Ss',
            'iX_4024Sp',
            'iX_4024Ss',
        )
    }),
    'M50': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 28,
        'front_loaded': True,
        'front_slots': 24,
        'rear_slots': 4,
        'expected_t10': (
            'ECStream_4024Sp',
            'ECStream_4024Ss',
            'iX_4024Sp',
            'iX_4024Ss',
        )
    }),
    'M60': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 28,
        'front_loaded': True,
        'front_slots': 24,
        'rear_slots': 4,
        'expected_t10': (
            'ECStream_4024Sp',
            'ECStream_4024Ss',
            'iX_4024Sp',
            'iX_4024Ss',
        )
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
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R20A': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R20B': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 14,
        'front_loaded': True,
        'front_slots': 14,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R30': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 16,
        'front_loaded': True,
        'front_slots': 12,
        'internal_slots': 4,
        'nvme_only': True,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R40': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 48,
        'top_loaded': True,
        'top_slots': 48,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R50': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 51,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 3,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R50B': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 50,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 2,
        'expected_t10': (
            'ECStream_FS1',
            'ECStream_FS2',
            'ECStream_DSS212Sp',
            'ECStream_DSS212Ss',
            'iX_FS1L',
            'iX_FS2',
            'iX_DSS212Sp',
            'iX_DSS212Ss',
            'iX_TrueNASR20p',
            'iX_2012Sp',
            'iX_TrueNASSMCSC826-P',
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
            'AHCI_SGPIOEnclosure',
        )
    }),
    'R50BM': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 52,
        'top_loaded': True,
        'top_slots': 48,
        'rear_slots': 4,
        'expected_t10': (
            'iX_eDrawer4048S1',
            'iX_eDrawer4048S2',
        )
    }),
    'X10': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 12,
        'front_loaded': True,
        'front_slots': 12,
        'expected_t10': ('CELESTIC_P3215-O', 'CELESTIC_P3217-B'),
    }),
    'X20': ModelInfo(**{
        'rackmount': True,
        'total_drive_bays': 12,
        'front_loaded': True,
        'front_slots': 12,
        'expected_t10': ('CELESTIC_P3215-O', 'CELESTIC_P3217-B'),
    }),
}
        t10vendor_product = f'{self.vendor}_{self.product}'
        match t10vendor_product:
            case 'AHCI_SGPIOEnclosure':
                # R20 variants or MINIs
                self.model = dmi_model.value
                self.controller = True
            case 'CELESTIC_X2012' | 'CELESTIC_X2012-MT':
                self.model = JbodModels.ES12.value
                self.controller = False
            case 'ECStream_4024J' | 'iX_4024J':
                self.model = JbodModels.ES24.value
                self.controller = False
            case 'ECStream_2024Jp' | 'ECStream_2024Js' | 'iX_2024Jp' | 'iX_2024Js':
                self.model = JbodModels.ES24F.value
                self.controller = False
            case 'CELESTIC_R0904-F0001-01':
                self.model = JbodModels.ES60.value
                self.controller = False
            case 'HGST_H4060-J':
                self.model = JbodModels.ES60G2.value
                self.controller = False
            case 'HGST_H4102-J':
                self.model = JbodModels.ES102.value
                self.controller = False
            case 'VikingES_NDS-41022-BB' | 'VikingES_VDS-41022-BB':
                self.model = JbodModels.ES102G2.value
                self.controller = False
            case _:
                logger.warning(
                    'Unexpected t10 vendor: %r and product: %r combination',
                    self.vendor, self.product
                )
                self.model = ''
                self.controller = False
