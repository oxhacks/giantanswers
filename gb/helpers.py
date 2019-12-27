"""Helpers to facilitate API interaction."""
from functools import wraps
from datetime import datetime


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


CACHE = {}
MAX_AGE = 60 * 60 * 24  # a day


def memoize_class(func):
    """Decorator to assist with the memoization of class methods."""
    @wraps(func)
    def wrapper(*args):
        expired = False
        sig = (func, args)
        cached, timestamp = CACHE.get(sig, (None, None,))
        if timestamp:
            age = datetime.utcnow() - timestamp
            if age.total_seconds() > MAX_AGE:
                expired = True
        if cached and not expired:
            return cached
        value = func(*args)
        CACHE[sig] = value, datetime.utcnow()
        return value
    return wrapper
