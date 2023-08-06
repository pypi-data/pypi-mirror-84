import typing as tp


def format_text(input: tp.Any) -> str:
    """Return custom text with input.
        
    :param input: Input from user.
    :return: f'my input: {input}'

    Sample:
    >>> format_text('Jane Doe')
    my input: Jane Doe
    >>> format_text(1)
    my input: 1
    """
    return f"my input: {input}"
