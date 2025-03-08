from zenml.pipelines import pipeline
from zenml.steps import step
import subprocess
import os
from zenml.client import Client


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'data', 'cosmetic.db')
CLEANED_DB_PATH = os.path.join(ROOT_DIR, 'data', 'cosmetic_cleaned.db')

@step
def ingest_data() -> str:
    ingestion_script = os.path.join(ROOT_DIR, 'data', 'ingestion.py')
    subprocess.run(["python3", ingestion_script])
    return DB_PATH

@step
def preprocess_data(db_path: str) -> str:
    preprocessing_script = os.path.join(ROOT_DIR, 'data', 'preprocessing.py')
    subprocess.run(["python3", preprocessing_script])
    return db_path

@step
def validate_data(db_path: str) -> str:
    validation_script = os.path.join(ROOT_DIR, 'data', 'data_validation.py')
    subprocess.run(["python3", validation_script])
    return CLEANED_DB_PATH

@pipeline
def skincare_pipeline():
    db_path = ingest_data()
    processed_db_path = preprocess_data(db_path)
    cleaned_db_path = validate_data(processed_db_path)
    return cleaned_db_path


if __name__ == "__main__":

    skincare_pipeline_instance = skincare_pipeline()

    client = Client()
    pipeline_run = skincare_pipeline_instance.run()  

    print(f"Pipeline run started: {pipeline_run}")