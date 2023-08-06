from pydantic import BaseModel, validator


class Operation(BaseModel):
    type: str
    value: str

    @validator("type")
    def must_be_types(cls, value):
        if value not in ["continuous", "discrete"]:
            raise ValueError("must be either 'discrete' or 'continuous'")
        return value
