import tokenize
import pytest
from flake8_length._parser import get_lines_info, TRUNCATE_TO


def to_tokens(lines: list):
    readline = (line.encode() for line in lines).__next__
    return list(tokenize.tokenize(readline))


@pytest.mark.parametrize('given, expected', [
    # regular code
    ('123', 3),
    ('12367', 5),

    # comments
    ('# hello', 7),
    ('# hello world', 13),
    ('# https://github.com/life4/deal', TRUNCATE_TO + 2),
])
def test_get_lines_info(given: str, expected: int):
    tokens = to_tokens([given])
    infos = list(get_lines_info(tokens[1]))
    assert len(infos) == 1
    assert infos[0].length == expected


@pytest.mark.parametrize('given', [
    ('#!/usr/bin/env python3'),
    ('# noqa: D12'),
    ('# pragma: no cover'),
    ('# E: Incompatible types in assignment'),
])
def test_skip(given: str):
    tokens = to_tokens([given])
    infos = list(get_lines_info(tokens[1]))
    assert len(infos) == 0
