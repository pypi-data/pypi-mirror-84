def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    """
    Replace first ocurrence from back of string.

    :param s:
    :param old:
    :param new:
    :param occurrence:
    :return:
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def remove_outside_brackets(s: str) -> str:
    """
    Remove starting and trailing round brackets from a string.

    Note: Whitespaces at beginning/end are *not* removed with `strip()`, function
    is supposed to also work with strings containing whitespaces.

    :param s: Input string.
    :return: The reformatted string.
    """

    if s.startswith('('):
        s = s.replace('(', '', 1)
    if s.endswith(')'):
        s = rreplace(s, ')', '', 1)

    return s
