from pydantic import root_validator


class BaseAtLeastOneFieldValidator:
    @root_validator(pre=True)
    def any_of(cls, v: dict) -> dict:
        filtered_values = {k: v for k, v in v.items() if v is not None}
        if len(filtered_values.values()) == 0:
            raise ValueError("at least one field is required")
        return v
