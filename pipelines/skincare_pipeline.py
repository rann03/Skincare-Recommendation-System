from zenml.pipelines import pipeline
from zenml.steps import step
import subprocess
import os
from zenml.client import Client
import dvc.api


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cosmetic.db')
CLEANED_DB_PATH = os.path.join(ROOT_DIR, 'data', 'cosmetic_cleaned.db')
versioned_db = os.path.join(ROOT_DIR, 'data', 'cosmetic_versioned.db')

@step(enable_cache=False)
def ingest_data() -> str:
    ingestion_script = os.path.join(ROOT_DIR, 'data', 'ingestion.py')
    subprocess.run(["python3", ingestion_script])
    return DB_PATH

@step(enable_cache=False)
def preprocess_data(db_path: str) -> str:
    preprocessing_script = os.path.join(ROOT_DIR, 'data', 'preprocessing.py')
    subprocess.run(["python3", preprocessing_script])
    return db_path

@step(enable_cache=False)
def validate_data(db_path: str) -> str:
    validation_script = os.path.join(ROOT_DIR, 'data', 'data_validation.py')
    subprocess.run(["python3", validation_script])
    return CLEANED_DB_PATH
@step
def version_data(cleaned_db_path: str) -> str:
    """
    Use DVC to track and push the cleaned database to remote storage.
    """
    # Add the cleaned database to DVC
    subprocess.run(["dvc", "add", cleaned_db_path], check=True)
    
    # Stage all changes
    subprocess.run(["git", "add", "-A"], check=True)
    
    # Commit the changes to Git
    subprocess.run(["git", "commit", "-m", "Track cleaned database with DVC"], check=True)
    
    # Push the data to the remote storage
    subprocess.run(["dvc", "push"], check=True)
    
    # Get the DVC URL for the remote version
    dvc_url = dvc.api.get_url(cleaned_db_path)
    print(f"Data versioned and pushed to remote: {dvc_url}")
    
    return dvc_url

@pipeline
def skincare_pipeline():
    db_path = ingest_data()
    processed_db_path = preprocess_data(db_path)
    cleaned_db_path = validate_data(processed_db_path)
    version_info = version_data(cleaned_db_path)
    return version_info


if __name__ == "__main__":

    skincare_pipeline_instance = skincare_pipeline()

    client = Client()
    pipeline_run = skincare_pipeline_instance  

    print(f"Pipeline run started: {pipeline_run}")







