from google.cloud import compute_v1

def list_instances(project_id, zone):
    client = compute_v1.InstancesClient()
    instances = client.list(project=project_id, zone=zone)
    for instance in instances:
        print(f"Name: {instance.name}, Status: {instance.status}")

if __name__ == "__main__":
    list_instances("devops-learning-505512", "asia-south1-a")

