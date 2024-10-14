#!/bin/bash
##############################
#
# Docker image update for nextcloud
#
##############################

# Logging into nextcloud directory
cd /home/user/docker-nextcloud
echo "Entering nextcloud folder ...."
# Stopping nextcloud container
echo "Stopping nextcloud containers ..."
docker stop nextcloud swag redis mariadb duckdns
# Updating nextcloud
echo "Updating docker image for nextcloud"
docker compose pull
# Starting nextcloud container
echo "Starting nextcloud containers .... "
docker compose up -d
