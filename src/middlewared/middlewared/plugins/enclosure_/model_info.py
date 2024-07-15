from dataclasses import dataclass


@dataclass(kw_only=True, slots=True, frozen=True)
class ModelInfo:
    rackmount: bool = False
    """Is this model rackmountable?"""
    total_drive_bays: int
    """Total number of drive bays."""
    top_loaded: bool = False
    """Do the disk bays get loaded from the top? For example,
    the 60/102 bay JBODs are top loaded."""
    top_slots: int = 0
    """Total number of top loaded disk bays."""
    front_loaded: bool = False
    """Do the disk bays get loaded from the front? For example,
    the F60 is front loaded."""
    front_slots: int = 0
    """Total number of front loaded disk bays."""
    rear_slots: int = 0
    """Total number of rear loaded drive bays."""
    internal_slots: int = 0
    """Total number of internal loaded drive bays."""
    nvme_only: bool = False
    """Is this model an NVMe only system?"""
    is_jbod: bool = False
    """Is this a JBoD (Just a Bunch of Disks)?"""
    is_jbof: bool = False
    """Is this a JBoF (Just a Bunch of Flash)?"""
    expected_t10: tuple[str] = tuple()
    """The EXPECTED strings for the T10 vendor, product, revision buffers
    returned from a standard SCSI inquiry command as defined in Table 148 of SBC-5."""
