import pandas as pd
from feast import FeatureStore
from features import cosmetic_features
from datetime import datetime

df = pd.read_parquet("../data/cosmetic_feature_data.parquet")

store = FeatureStore(repo_path=".")

store.apply([cosmetic_features])

store.materialize_incremental(end_date=datetime.utcnow())








