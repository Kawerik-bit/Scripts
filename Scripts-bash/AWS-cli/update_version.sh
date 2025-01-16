#!/bin/bash

# Getting information from the user
echo "Enter the cluster name: "
read -r cluster
echo "Enter the node group name: "
read -r node_group
echo "Enter the AWS region: "
read -r region
echo "Enter the desired EKS Kubernetes version: "
read -r version

# Updating control plane
echo "Starting control plane update..."
if aws eks update-cluster-version --name "$cluster" --region "$region" --kubernetes-version "$version"; then
    echo "Control plane update initiated."
else
    echo "Failed to initiate control plane update. Please check the input values or AWS permissions."
    exit 1
fi

# Check control plane status
status=$(aws eks describe-cluster --name "$cluster" --region "$region" --query "cluster.status" --output text)
while [[ "$status" == "UPDATING" ]]; do
    echo "Control plane is still updating..."
    sleep 5
    status=$(aws eks describe-cluster --name "$cluster" --region "$region" --query "cluster.status" --output text)
done

if [[ "$status" == "ACTIVE" ]]; then
    echo "Control plane update completed successfully with status: $status"
else
    echo "Control plane update failed with status: $status"
    exit 1
fi

# Updating node group
echo "Starting node group update..."
if aws eks update-nodegroup-version --cluster-name "$cluster" --region "$region" --nodegroup-name "$node_group" --kubernetes-version "$version"; then
    echo "Node group update initiated."
else
    echo "Failed to initiate node group update. Please check the input values or AWS permissions."
    exit 1
fi

# Check node group status
status=$(aws eks describe-nodegroup --cluster-name "$cluster" --region "$region" --nodegroup-name "$node_group" --query "nodegroup.status" --output text)
while [[ "$status" == "UPDATING" ]]; do
    echo "Node group is still updating..."
    sleep 5
    status=$(aws eks describe-nodegroup --cluster-name "$cluster" --region "$region" --nodegroup-name "$node_group" --query "nodegroup.status" --output text)
done

if [[ "$status" == "ACTIVE" ]]; then
    echo "Node group update completed successfully with status: $status"
else
    echo "Node group update failed with status: $status"
    exit 1
fi

echo "EKS cluster and node group successfully updated to version $version."
