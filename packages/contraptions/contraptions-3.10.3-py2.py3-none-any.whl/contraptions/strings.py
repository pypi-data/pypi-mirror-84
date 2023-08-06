import random


def scramble(input: str) -> str:
    """Scrambles a word like the spongebob meme."""
    x = list(input)
    y = []
    for char in x:
        if char == " ":
            y.append(" ")
        else:
            char = char.lower()
            if random.choice([True, False]):
                char = char.upper()
            y.append(char)

    return (" ".join(y)).strip()
