from pydantic import BaseModel


class TimeFormat(BaseModel):
    hour: int
    minute: int
    second: int
