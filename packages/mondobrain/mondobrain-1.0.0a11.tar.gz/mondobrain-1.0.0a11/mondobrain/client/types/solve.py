from io import BytesIO
from typing import Dict, List, Union

from pydantic import StrictFloat, StrictInt, StrictStr

from mondobrain.types import Rule, SolveOptions

from .base import BaseOptions, BaseResponse

__all__ = [
    "StartOptions",
    "StartResponse",
    "StartFileOptions",
    "StartFileResponse",
    "ResultOptions",
    "ResultResponse",
]


#######################
# SOLVE.START
#######################
class StartOptions(BaseOptions, SolveOptions):
    """StartOptions defines the options able to be passed to solve.start"""

    data: List[Dict[str, Union[None, StrictStr, StrictInt, StrictFloat]]]


class StartResponse(BaseResponse):
    """StartResponse defines the 200 response from solve.start"""

    id: str


#######################
# SOLVE.START.FILE
#######################
class StartFileOptions(BaseOptions, SolveOptions):
    """StartFileOptions defines the options able to be passed to solve.start.file"""

    data: BytesIO

    class Config:
        arbitrary_types_allowed = True


class StartFileResponse(BaseResponse):
    """StartFileResponse defines the 200 response from solve.start.file"""

    id: str


#######################
# SOLVE.RESULT
#######################
class ResultOptions(BaseOptions):
    """ResultOptions defines the options able to be passed to solve.result"""

    id: str


class ResultResponse(BaseResponse):
    """ReusltResponse defines the 200 response from solve.result"""

    rule: Rule
