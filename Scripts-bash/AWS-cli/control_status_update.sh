#!/bin/bash

# Fetch the status of the nodegroup
status=$(aws eks describe-cluster --name <cluster> --region <region> --query "cluster.status" --output text)

# Loop until the status is no longer "UPDATING"
while [[ "$status" == "UPDATING" ]]; do
    echo "Control plane is still updating..."
    sleep 5
    status=$(aws eks describe-cluster --name <cluster> --region <region> --query "cluster.status" --output text)
done

echo "Control plane update completed with status: $status"
