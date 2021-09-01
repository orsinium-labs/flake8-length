# built-in
import tokenize

# external
import pytest
from typing import Union, List
# project
from flake8_length._parser import TRUNCATE_TO, get_lines_info


def to_tokens(lines: List[str]):
    readline = (line.encode() for line in lines).__next__
    return list(tokenize.tokenize(readline))


@pytest.mark.parametrize('given, expected', [
    # regular code
    ('123', [3]),
    ('12367', [5]),

    # comments
    ('# hello', [7]),
    ('# hello world', [13]),
    ('# https://github.com/life4/deal', [TRUNCATE_TO + 2]),
    ('# see also: https://github.com/life4/deal', [TRUNCATE_TO + 12]),

    # strings
    ('"SELECT * FROM table"', [21]),
    ('"SELECT * FROM table_with_very_long_name"', [TRUNCATE_TO + 15]),

    # multiline strings
    (
        "'''\n  hello world\n'''",
        [3, 13, 3],
    ),
    (
        "'''\n  https://github.com/life4/deal\n'''",
        [3, TRUNCATE_TO + 2, 3],
    ),
    (
        ("print('''\n", ' 1' * 39 + '\n', "''')\n"),
        # 5, 6, 9 = three tokens in print('''
        # 78 = length of ' 1'*39
        # 3, 4 = two tokens in ''')
        [5, 6, 9, 78, 3, 4]
    ),
])
def test_get_lines_info(given: Union[str, List[str]], expected: int):
    if isinstance(given, str):
        given = [given]

    tokens = to_tokens(given)
    print(*tokens, sep='\n')
    infos: list = []
    for token in tokens:
        infos.extend(get_lines_info(token))
    assert [info.length for info in infos] == expected


@pytest.mark.parametrize('given', [
    '#!/usr/bin/env python3',
    '# noqa: D12',
    '# pragma: no cover',
    '# E: Incompatible types in assignment',
    '"hello"',
])
def test_skip(given: str):
    tokens = to_tokens([given])
    infos = list(get_lines_info(tokens[1]))
    assert len(infos) == 0
