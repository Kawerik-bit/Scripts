from kubernetes import client, config
import time

config.load_kube_config()
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def start_deployment(namespace, deployment_name):
    """Start a Kubernetes deployment."""
    try:
        # Scales the deployment to 1
        apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace, {'spec': {'replicas': 1}})
        print(f"Started deployment {deployment_name} in namespace {namespace}.")
    except Exception as e:
        print(f"Error starting deployment: {e}")

def stop_deployment(namespace, deployment_name):
    """Stop a Kubernetes deployment."""
    try:
        # Scales the deployment to 0
        apps_v1.patch_namespaced_deployment_scale(deployment_name, namespace, {'spec': {'replicas': 0}})
        print(f"Stopped deployment {deployment_name} in namespace {namespace}.")
    except Exception as e:
        print(f"Error stopping deployment: {e}")

def monitor_and_restart_pods(namespace):
    """Monitor pods and restart them if they fail."""
    while True:
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            if pod.status.phase == "Failed":
                print(f"Pod {pod.metadata.name} has failed. Restarting...")
                # Deletes the failed pod to force a restart
                v1.delete_namespaced_pod(pod.metadata.name, namespace)
                print(f"Deleted pod {pod.metadata.name}.")
        
        time.sleep(10)  # Checks every 10 seconds

def cleanup_unused_resources(namespace):
    """Clean up unused pods and images in a namespace."""
    # Deletes completed pods
    completed_pods = v1.list_namespaced_pod(namespace, watch=False, label_selector="status.phase=Succeeded")
    for pod in completed_pods.items:
        print(f"Deleting completed pod {pod.metadata.name}.")
        v1.delete_namespaced_pod(pod.metadata.name, namespace)

    # Deletes failed pods
    failed_pods = v1.list_namespaced_pod(namespace, watch=False, label_selector="status.phase=Failed")
    for pod in failed_pods.items:
        print(f"Deleting failed pod {pod.metadata.name}.")
        v1.delete_namespaced_pod(pod.metadata.name, namespace)

def main():
    namespace = input("input_namespace_you_want_to_run_this_on")
    
    while True:
        print("\n1. Start Deployment")
        print("2. Stop Deployment")
        print("3. Monitor and Restart Pods")
        print("4. Cleanup Unused Resources")
        print("5. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            deployment_name = input("Enter the deployment name to start: ")
            start_deployment(namespace, deployment_name)
        elif choice == '2':
            deployment_name = input("Enter the deployment name to stop: ")
            stop_deployment(namespace, deployment_name)
        elif choice == '3':
            print("Monitoring pods in the background...")
            monitor_and_restart_pods(namespace)
        elif choice == '4':
            cleanup_unused_resources(namespace)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

# Kubernetes management script - run with "python3 k8s_standard.py"
