from pydantic import root_validator


class BaseAtLeastOneFieldValidator:
    @root_validator(pre=True)
    def any_of(cls, v: dict) -> dict:
        if len(v.values()) == 0 or any(v.values()) is False:
            raise ValueError("at least one field is required")
        return v
