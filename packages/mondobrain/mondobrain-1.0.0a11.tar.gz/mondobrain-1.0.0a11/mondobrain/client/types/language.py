from typing import List

from pydantic import BaseModel

from mondobrain.types import EntitiesMetadata, Operation

from .base import BaseOptions, BaseResponse

__all__ = ["EntitiesOptions", "EntitiesResponse"]


#######################
# LANGUAGE.ENTITIES
#######################
class EntitiesSubDict(BaseModel):
    explorable: List[str]
    outcome: str
    operation: Operation
    constraints: List[str]


class EntitiesOptions(BaseOptions):
    """EntitiesOptions defines the options able to be passed to language.entities"""

    message: str
    metadata: EntitiesMetadata


class EntitiesResponse(BaseResponse):
    """EntitiesResponse defines the 200 response from language.entities"""

    entities: EntitiesSubDict
