from pydantic import BaseModel, Extra


class BaseOptions(BaseModel):
    class Config:
        extra: Extra.allow


class BaseResponse(BaseModel):
    ok: bool = None

    class Config:
        extra: Extra.allow


class BaseError(BaseResponse):
    ok = False
    type: str
    code: str = None
    message: str
