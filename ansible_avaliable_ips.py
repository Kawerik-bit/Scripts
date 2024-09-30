import re
import ipaddress

# Configuration
ANSIBLE_HOST_FILE = '/usr/bin/ansible/ansible_hosts'  
IP_POOL = '192.168.1.0/24'                         # Change this to the IP pool you want to check

def read_ansible_hosts(file_path):
    """Read the Ansible hosts file and return its content."""
    with open(file_path, 'r') as file:
        return file.readlines()

def extract_used_ips(hosts_content):
    """Extract IP addresses from the hosts content via regex."""
    used_ips = set()
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')  # Regular expression for matching IPs

    for line in hosts_content:
        matches = ip_pattern.findall(line)
        used_ips.update(matches)

    return used_ips

def get_available_ips(ip_pool, used_ips):
    """Determine available free IP addresses in the pool."""
    network = ipaddress.ip_network(ip_pool, strict=False)  # Create an IP network object
    available_ips = []

    for ip in network.hosts():  # Iterate through all usable IPs in the network
        if str(ip) not in used_ips:  # If not in used IPs, add to available list
            available_ips.append(str(ip))

    return available_ips

def main():
    """ find and print available IPs."""
    # Read the Ansible hosts file
    hosts_content = read_ansible_hosts(ANSIBLE_HOST_FILE)

    # Extract used IPs
    used_ips = extract_used_ips(hosts_content)
    print("Used IPs:", used_ips)

    # Get available IPs
    available_ips = get_available_ips(IP_POOL, used_ips)
    print("Available IPs:", available_ips)

if __name__ == '__main__':
    main()
# Excute script with "python3 ansible_avaliable_ips.py"
# This script will return all avaliable/free or not used IPs in the ansible host file based on the network range
