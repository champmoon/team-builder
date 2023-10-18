def check_three_unique_symbols(v: str) -> str:
    assert len(set(v)) >= 3, "password must contain 3 unique ascii letters"

    return v


def only_ascii_letters(v: str) -> str:
    try:
        v.encode("ascii")
    except UnicodeEncodeError:
        assert False, "password must contain only ascii letters"
    return v
