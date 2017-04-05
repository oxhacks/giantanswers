"""Helpers to facilitate API interaction."""


# Spoken strings come to us as words, not numbers.
NUM_WORD_INT = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

# The same thing as NUM_WORD_INT, but already stringified.
NUM_WORD_STRING = {k: str(v) for k, v in NUM_WORD_INT.items()}


def word_to_int(phrase, mapping=NUM_WORD_STRING):
    """Take a phrase and replace the number words in it with their digits.
    
    :param phrase: the phrase to mogrify
    :param mapping: the mapping of number words to number digits
    :returns: the phrase with replacements made
    
    """
    tokens = phrase.split()
    for token in tokens:
        if token in mapping:
            phrase = phrase.replace(token, mapping[token])
    return phrase