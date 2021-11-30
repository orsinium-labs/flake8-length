# built-in
import re
import tokenize
from pathlib import Path

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

    # ignored endline markers
    ('123', [3]),
    ('123,', [3]),
    ('[123]', [4]),
    ('(123)', [4]),
    ('(123,)', [4]),
    ('(123,);', [4]),
    ('if 0:0', [2, 4, 6]),

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
        [5, 9, 78, 3]
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


def test_fixture():
    path = Path(__file__).parent / 'fixture.py'
    lines = path.read_text().splitlines()

    rex = re.compile(r'  # L(\d+)')
    cleaned = []
    expected = {}
    for i, line in enumerate(lines, start=1):
        match = rex.search(line)
        if match:
            line = line.replace(match.group(0), ' ')
            expected[i] = int(match.group(1))
        cleaned.append(line.rstrip(' ') + '\n')
    assert len(expected) > 5

    actual = {}
    for token in to_tokens(cleaned):
        for info in get_lines_info(token):
            actual[info.row] = max(
                info.length,
                actual.get(info.row, 0),
            )
    assert actual == expected
