import os
import shutil
import datetime
import logging
import smtplib
from email.mime.text import MIMEText

SOURCE_DIR = "/home/kawerik/"  
BACKUP_DIR = "/home/kawerik/Documents/backups"                  
LOG_FILE = "/home/kawerik/Documents/backupsbackup.log"  
EMAIL_ALERT = "kawerik-bit@test.com"  

# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_email_alert(error_message):
    msg = MIMEText(f"Backup failed with the following error:\n\n{error_message}")
    msg['Subject'] = "Backup Script Alert"
    msg['From'] = "backup_script@example.com"
    msg['To'] = EMAIL_ALERT

    try:
        with smtplib.SMTP('localhost') as server: 
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def backup():
    try:
        date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = os.path.join(BACKUP_DIR, date_str)
        os.makedirs(backup_path)

        shutil.copytree(SOURCE_DIR, backup_path)

        logging.info(f"Backup of '{SOURCE_DIR}' completed successfully to '{backup_path}'.")

    except Exception as e:
        logging.error(f"Backup of '{SOURCE_DIR}' failed: {e}")
        send_email_alert(e)

if __name__ == "__main__":
    backup()


# To execute run in terminal: "python3 backup.py" Make sure python3 is installed.
# Could also be scheduled as a cronjob to further automate it: "crontab -e" and "0 5 * * * /usr/bin/python3 /home/kawerik/scripts/backup.py"
# Th above example sets the cronjob for 05:00 AM
