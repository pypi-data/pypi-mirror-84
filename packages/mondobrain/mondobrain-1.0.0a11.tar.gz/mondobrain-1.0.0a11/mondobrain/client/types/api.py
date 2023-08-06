from .base import BaseOptions, BaseResponse

__all__ = ["TestOptions", "TestResponse"]


#######################
# API.TEST
#######################
class TestOptions(BaseOptions):
    """TestOptions defines the options able to be passed to api.test"""

    error: str = None


class TestResponse(BaseResponse):
    """TestResponse defines the 200 response from api.test"""

    error: str = None
