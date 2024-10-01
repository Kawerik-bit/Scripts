import os
import subprocess
import time
import logging
import smtplib
from email.mime.text import MIMEText

CRITICAL_SERVICES = ['x.x.x.x', 'y.y.y.y']  # IPs to be monitored
LOG_FILE = '/var/log/network_latency.log'  # Path to the loging file
PING_COUNT = 6  # ping test attempts
LATENCY_THRESHOLD = 125  # Latency threshold in milliseconds
PACKET_LOSS_THRESHOLD = 30  # Packet loss in percentages
CHECK_INTERVAL = 30  # Time between checks in seconds

# Alerts for email configuration
EMAIL_ALERTS_ENABLED = True  # Can be set to False if you want to dissable
SMTP_SERVER = 'smtp.test.com'
SMTP_PORT = 587
EMAIL_FROM = 'monitor@test.com'
EMAIL_TO = 'admin@test.com'
EMAIL_SUBJECT = 'Network Performance Alarm'
EMAIL_USERNAME = 'smtp_username'
EMAIL_PASSWORD = 'smtp_password'

# logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_email_alert(service, latency, packet_loss):
    """Send an email alert for network performance issues."""
    if not EMAIL_ALERTS_ENABLED:
        return

    msg_body = f"Network performance issue detected for {service}.\n\n" \
               f"Latency: {latency} ms\nPacket Loss: {packet_loss}%\n"
    msg = MIMEText(msg_body)
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = EMAIL_SUBJECT

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        logging.info(f"Alert email sent for {service}.")
    except Exception as e:
        logging.error(f"Error: Failed to send alert email: {e}")

def ping_service(service):
    """Ping a network service and return latency and packet loss results."""
    try:
        # ping command
        result = subprocess.run(
            ['ping', '-c', str(PING_COUNT), service],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            logging.warning(f"Failed to ping {service}. Error: {result.stderr}")
            return None, None

        # Take latency and packet loss from the ping output
        output = result.stdout
        latency = extract_latency(output)
        packet_loss = extract_packet_loss(output)
        return latency, packet_loss

    except Exception as e:
        logging.error(f"Error pinging {service}: {e}")
        return None, None

def extract_latency(ping_output):
    """Extract the average latency from ping output."""
    lines = ping_output.split('\n')
    for line in lines:
        if 'rtt min/avg/max' in line:
            avg_latency = line.split('/')[4]
            return float(avg_latency)
    return None

def extract_packet_loss(ping_output):
    """Extract the packet loss percentage from ping output."""
    lines = ping_output.split('\n')
    for line in lines:
        if 'packet loss' in line:
            packet_loss_str = line.split(', ')[2]
            packet_loss = float(packet_loss_str.split('%')[0])
            return packet_loss
    return None

def monitor_services():
    """Monitor the critical network services and log performance."""
    while True:
        for service in CRITICAL_SERVICES:
            latency, packet_loss = ping_service(service)
            if latency is not None and packet_loss is not None:
                logging.info(f"Service: {service}, Latency: {latency} ms, Packet Loss: {packet_loss}%")

                # Check if the latency or packet loss exceeds the set threshold
                if latency > LATENCY_THRESHOLD or packet_loss > PACKET_LOSS_THRESHOLD:
                    logging.warning(f"Performance issue detected for {service}: Latency = {latency} ms, Packet Loss = {packet_loss}%")
                    send_email_alert(service, latency, packet_loss)

        # Sleep until next interval
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    logging.info("Starting network performance monitoring...")
    try:
        monitor_services()
    except KeyboardInterrupt:
        logging.info("Network monitoring stopped.")

# Run script - python3 monit-network.py
# Make sure to psutil is installed on the machine in order for the script to work
# Installation: "pip install psutil"
