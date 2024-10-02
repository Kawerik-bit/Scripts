import shutil
import psutil
from network import check_localhost, check_connectivity

def check_disk_usage(disk='/'):
    """Verifies that there's enough free space on the specified disk."""
    try:
        du = shutil.disk_usage(disk)
        free = du.free / du.total * 100
        return free > 20  # informs if space is above 20%
    except Exception as e:
        print(f"Error checking disk usage: {e}")
        return False

def check_cpu_usage():
    """Verifies that there's enough unused CPU."""
    try:
        usage = psutil.cpu_percent(interval=1)
        return usage < 75  # informs if CPU usage is less than 75%
    except Exception as e:
        print(f"Error checking CPU usage: {e}")
        return False

if __name__ == "__main__":
    if not check_disk_usage('/') or not check_cpu_usage():
        print("ERROR: Insufficient resources!")
    elif check_localhost() and check_connectivity():
        print("Everything is okay.")
    else:
        print("ERROR: Network checks failed.")
      
# Execute with "python3 old_health_check.py"
