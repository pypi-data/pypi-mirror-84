from .base import BaseOptions, BaseResponse

__all__ = ["TestOptions", "TestResponse"]


#######################
# AUTH.TEST
#######################
class TestOptions(BaseOptions):
    """TestOptions defines the options able to be passed to auth.test"""

    error: str = None


class TestResponse(BaseResponse):
    """TestResponse defines the 200 response from auth.test"""

    error: str = None
