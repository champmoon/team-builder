from typing import Annotated

from pydantic import AfterValidator

from .funcs import check_three_unique_symbols, only_ascii_letters

Password = Annotated[
    str,
    AfterValidator(check_three_unique_symbols),
    AfterValidator(only_ascii_letters),
]
