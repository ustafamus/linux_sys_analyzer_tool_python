import speedtest
import psutil



def measure_speed():
    try:
     st = speedtest.Speedtest()
     st.get_best_server()
     download_speed = st.download() / 1_000_000  # Mbps cinsinden
     upload_speed = st.upload() / 1_000_000  # Mbps cinsinden
     ping = st.results.ping
     return download_speed, upload_speed, ping
    except speedtest.SpeedtestException:
     print("İnternet bağlantısı bulunamadı.")
     return None, None, None


def get_external_disks():
    external_disks = []
    for partition in psutil.disk_partitions():
        if partition.fstype not in ['squashfs','ext4'] and (partition.fstype in 'vfat' or 'nfts'):
            usage = psutil.disk_usage(partition.mountpoint)
            external_disks.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
    return external_disks
def print_ascii_art():
    ascii_art = """
 █████  ███    ██  █████  ██      ██ ███████     ██████  ██████   ██████   ██████  ██████   █████  ███    ███ ██ 
██   ██ ████   ██ ██   ██ ██      ██    ███      ██   ██ ██   ██ ██    ██ ██       ██   ██ ██   ██ ████  ████ ██ 
███████ ██ ██  ██ ███████ ██      ██   ███       ██████  ██████  ██    ██ ██   ███ ██████  ███████ ██ ████ ██ ██ 
██   ██ ██  ██ ██ ██   ██ ██      ██  ███        ██      ██   ██ ██    ██ ██    ██ ██   ██ ██   ██ ██  ██  ██ ██ 
██   ██ ██   ████ ██   ██ ███████ ██ ███████     ██      ██   ██  ██████   ██████  ██   ██ ██   ██ ██      ██ ██ 
    """
    print("*" * 80)
    print(ascii_art)
    print("*" * 80)
def main():
    print_ascii_art()
    external_disks = get_external_disks()
    if external_disks:
        for disk in external_disks:
            print("***EXTERNAL DISK***")
            print(f"Device: {disk['device']}")
            print(f"Mountpoint: {disk['mountpoint']}")
            print(f"File system type: {disk['fstype']}")
            print(f"Total size: {disk['total'] / (1024 ** 3):.2f} GB")
            print(f"Used space: {disk['used'] / (1024 ** 3):.2f} GB")
            print(f"Free space: {disk['free'] / (1024 ** 3):.2f} GB")
            print(f"Usage percentage: {disk['percent']}%")
            print("")
    else:
        print("No external disks found.")

    internal_disk = psutil.disk_usage("/")
    total_bytes = internal_disk.total
    used_bytes = internal_disk.used
    free_bytes = internal_disk.free
    percentage_disk = internal_disk.percent
    total_gigabytes = total_bytes / (1024 ** 3)
    used_gigabytes = used_bytes / (1024 ** 3)
    free_gigabytes = free_bytes / (1024 ** 3)


    print("***INTERNAL DISK***")
    print(f'Total disk space: {total_gigabytes:.2f} GB')
    print(f'Used disk space:{used_gigabytes:.2f} GB')
    print(f'Free disk space:{free_gigabytes:.2f} GB')
    print(f'Internal disk usage percent:{percentage_disk}%')
    print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/")
    print("")
    print("internet hizi hesaplaniyor...")
    download_speed, upload_speed, ping = measure_speed()
    if download_speed is not None and upload_speed is not None and ping is not None:
        print(f"İndirme Hızı: {download_speed:.2f} Mbps")
        print(f"Yükleme Hızı: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} ms")
    else:
        print("İnternet hızı ölçümü yapılamadı.")


if __name__ == "__main__":
    main()
