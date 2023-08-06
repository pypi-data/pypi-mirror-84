from typing import List, Tuple, Union

from pydantic import BaseModel, validator


class FeatureBase(BaseModel):
    key: str
    type: str

    @validator("type")
    def must_be_types(cls, value):
        if value not in ["continuous", "discrete"]:
            raise ValueError("must be either 'discrete' or 'continuous'")
        return value


class ContinuousFeature(FeatureBase):
    type = "continuous"
    range: Tuple[float, float]


class DiscreteFeature(FeatureBase):
    type = "discrete"
    modalities: List[str]


class EntitiesMetadata(BaseModel):
    """EntitiesMetadata defines the metadata passed to language.entities"""

    features: List[Union[ContinuousFeature, DiscreteFeature]]
    shape: Tuple[int, int]
