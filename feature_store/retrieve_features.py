from feast import FeatureStore
import pandas as pd


store = FeatureStore(repo_path=".")


entity_df = pd.DataFrame.from_dict({"cosmetic_id": [1001, 1002]})

features = store.get_historical_features(
    entity_df=entity_df,
    feature_refs=[
        "cosmetic_features:price",
        "cosmetic_features:rating",
        "cosmetic_features:reviews_count",
    ],
).to_df()

print(features)





