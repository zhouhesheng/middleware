from middlewared.test.integration.utils import call


def test_optimal_disk_usage():
    disk = call('disk.get_unused')[0]
    swap_size = 1024 * 1024 * 1024
    bios_boot = 1 * 1024 * 1024
    efi = 512 * 1024 * 1024
    gpt_align = 73 * 512
    data_size = disk['size'] - bios_boot - efi - swap_size - gpt_align
    # Will raise an exception if we fail to format the disk with given harsh restrictions
    call('boot.format', disk['name'], {'size': data_size, 'swap_size': swap_size})
