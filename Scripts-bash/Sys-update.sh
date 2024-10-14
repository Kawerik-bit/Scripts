#!/bin/bash
###########################
#
# System update script
#
##########################
# System update
apt update
# System upgrade
apt upgrade -y
# Autoremove
apt autoremove -y
# Reboot check
if [ -f /var/run/reboot-required ]; then
    echo 'Please Reboot!'
    reboot now
fi
