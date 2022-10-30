from tokenize import tokenize
from flake8_length import Checker


def test_checker():
    lines = [
        b'# hello world',
        b'# ' + b'ab cd' * 40,
    ]
    tokens = tokenize(iter(lines).__next__)
    checker = Checker(None, tokens)
    res = list(checker.run())
    assert res == [
        (2, 90, 'LN002 doc/comment line is too long (202 > 90)', Checker)
    ]
