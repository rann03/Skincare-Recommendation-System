import os
import sqlite3
import pandas as pd
import hashlib
import json
import dvc.api
from datetime import datetime

class DataVersionTracker:
    def __init__(self, db_path, version_log_path, dvc_repo_path=None):
        self.db_path = db_path
        self.version_log_path = version_log_path
        self.dvc_repo_path = dvc_repo_path

    def _calculate_data_hash(self):
        """
        Calculate a hash of the database contents to track changes
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            hash_md5 = hashlib.md5()

            for table in tables:
                table_name = table[0]
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                df_sorted = df.sort_values(by=df.columns.tolist()).reset_index(drop=True)
                
                hash_md5.update(df_sorted.to_string().encode('utf-8'))

        finally:
            conn.close()

        return hash_md5.hexdigest()

    def log_version(self, stage):
        """
        Log version information including DVC tracking
        """
        version_info = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'data_hash': self._calculate_data_hash(),
            'total_records': self._count_total_records(),
            'dvc_version': self._get_dvc_version()  # DVC version metadata
        }

        # Ensure version log exists
        if not os.path.exists(self.version_log_path):
            with open(self.version_log_path, 'w') as f:
                json.dump([], f)

        with open(self.version_log_path, 'r') as f:
            versions = json.load(f)

        versions.append(version_info)

        with open(self.version_log_path, 'w') as f:
            json.dump(versions, f, indent=4)

        print(f"Logged version: {version_info}")
        return version_info

    def _get_dvc_version(self):
        """
        Get the current DVC version of the tracked file (cosmetic.db).
        """
        if self.dvc_repo_path:
            try:
                version = dvc.api.get_url(self.db_path, repo=self.dvc_repo_path)
                return version
            except Exception as e:
                print(f"Error retrieving DVC version: {e}")
                return "Error retrieving DVC version"
        return "No DVC tracking"

    def _count_total_records(self):
        """
        Count total records across all tables
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            total_records = 0
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_records += cursor.fetchone()[0]

            return total_records
        finally:
            conn.close()

def track_database_version(db_path, stage_name='unknown', version_log_path=None, dvc_repo_path=None):
    """
    Function to track database version with DVC integration.
    
    :param db_path: Path to the database file
    :param stage_name: Name of the pipeline stage
    :param version_log_path: Optional path for version log
    :param dvc_repo_path: Path to the DVC repository for version tracking
    :return: Version information
    """
    if version_log_path is None:
        version_log_path = os.path.join(
            os.path.dirname(db_path), 
            'data_version_log.json'
        )

    tracker = DataVersionTracker(db_path=db_path, version_log_path=version_log_path, dvc_repo_path=dvc_repo_path)
    return tracker.log_version(stage=stage_name)