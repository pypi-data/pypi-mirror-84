import random
from string import ascii_lowercase as string_ascii_lowercase
from string import ascii_uppercase as string_ascii_uppercase
from string import punctuation as string_punctuation


def randstr(
    min_length: int = 5,
    max_length: int = 25,
    min_tokens: int = 1,
    max_tokens: int = 5,
    lowercase_letters: bool = True,
    uppercase_letters: bool = True,
    punctuation: bool = True,
    numbers: bool = True,
) -> str:
    """Return a single string generated from random characters according to the given parameters.

    Keyword Arguments:
        min_length {int} -- minimum total character length (default: {5})
        max_length {int} -- maximum total character length  (default: {25})
        min_tokens {int} -- minimum total tokens/words (default: {1})
        max_tokens {int} -- maximum total tokens/words (default: {5})
        lowercase_letters {bool} -- allow lowercase letters (default: {True})
        uppercase_letters {bool} -- allow uppercase letters (default: {True})
        punctuation {bool} -- allow punctuation characters (default: {True})
        numbers {bool} -- allow numbers (default: {True})

    Returns:
        str -- generated string
    """

    # Validate parameters
    if min_length > max_length:
        raise ValueError("'min_length' cannot be > 'max_length'")
    if min_tokens > max_tokens:
        raise ValueError("'min_tokens' cannot be > 'max_tokens'")
    for value in [
        min_tokens,
        max_tokens,
        min_length,
        max_length,
    ]:
        if value < 1:
            raise ValueError(value, "Value must be > 1")
    if min_tokens * 2 - 1 > max_length:
        raise ValueError(
            f"Cannot generate a string with "
            f"min_tokens={min_tokens} and max_length={max_length}"
        )

    # Create population
    char_population: list = []
    if lowercase_letters:
        char_population += string_ascii_lowercase
    if uppercase_letters:
        char_population += string_ascii_uppercase
    if punctuation:
        char_population += string_punctuation
    if numbers:
        char_population += "".join([str(n) for n in range(9)])

    # Create
    num_tokens = random.randint(min_tokens, max_tokens)
    while num_tokens * 2 - 1 > max_length:
        num_tokens -= 1
    assert num_tokens >= min_tokens
    str_length = random.randint(max([min_length, num_tokens * 2 - 1]), max_length)
    num_spaces = num_tokens - 1
    num_chars = str_length - num_spaces
    tokens = [random.choice(char_population) for _ in range(num_tokens)]
    for _ in range(num_chars - num_tokens):
        index = random.randint(0, num_tokens - 1)
        tokens[index] += random.choice(char_population)
    return " ".join(tokens)
