import subprocess
import logging

# Set up logging

LOG_FILE = '/var/log/postgresql/restart.log'  # Log file path
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def restart_postgres():
    """Restart the PostgreSQL service."""
    try:
        logging.info("Attempting to restart PostgreSQL service...")
        # Restart PostgreSQL using systemctl
        subprocess.run(['sudo', 'systemctl', 'restart', 'postgresql'], check=True)
        logging.info("PostgreSQL service restarted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to restart PostgreSQL: {e}")

if __name__ == "__main__":
    restart_postgres()
# Create Cronjob or schedule with jenkins to run this occasionally on specific database to restart it
# To set as cronjob: "0 6 * * 6 [ "$(date +\%m)" = "01" ] || [ "$(date +\%m)" = "07" ] && /usr/bin/python3 /home/kawerik/scripts/database_restart.py"
