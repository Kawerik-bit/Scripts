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

#execute sith "./Sys-update.sh"
# execute it while being in the directory of the script or specify the path to it
