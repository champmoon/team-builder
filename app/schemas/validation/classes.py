from pydantic import root_validator


class BaseAtLeastOneFieldValidator:
    @root_validator(pre=True)
    def any_of(cls, v: dict) -> dict:
        for field in v.values():
            if field is not None:
                return v
        return v
