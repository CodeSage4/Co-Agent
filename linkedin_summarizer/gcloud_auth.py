from google.cloud import storage


def authenticate_implicit_with_adc(project_id="multi-agent-library"):
    """
    Authenticate using Application Default Credentials (ADC) and list storage buckets.
    
    Args:
        project_id: The project ID of your Google Cloud project.
    """
    try:
        # Initialize the Cloud Storage client
        storage_client = storage.Client(project=project_id)
        
        # List all buckets in the project
        buckets = storage_client.list_buckets()
        print("Buckets:")
        for bucket in buckets:
            print(bucket.name)
        print("Listed all storage buckets.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace with your Google Cloud project ID
authenticate_implicit_with_adc(project_id="multi-agent-library")
