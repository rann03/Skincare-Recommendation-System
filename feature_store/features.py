from feast import Entity, FeatureView, Field
from feast.data_source import FileSource
from feast.types import Float32, Int64


cosmetics_data = FileSource(
    path="data/cosmetic_feature_data.parquet",
    event_timestamp_column="event_timestamp",
)

cosmetic = Entity(name="cosmetic_id", join_keys=["cosmetic_id"])

cosmetic_features = FeatureView(
    name="cosmetic_features",
    entities=[cosmetic],
    ttl=None,
    schema=[
        Field(name="price", dtype=Float32),
        Field(name="rating", dtype=Float32),
        Field(name="reviews_count", dtype=Int64),
    ],
    online=True,
    source=cosmetics_data,
)