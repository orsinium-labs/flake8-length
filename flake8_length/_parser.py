import re
import tokenize
from typing import Iterator, NamedTuple


REX_NOQA = re.compile(r'(noqa|[nwer]:|pragma:).+')
TRUNCATE_TO = 10


class LineInfo(NamedTuple):
    row: int
    length: int


def get_line_length(line: str) -> int:
    chunks = line.split()
    if not chunks:
        return len(line)
    last_chunk_size = len(chunks[-1])
    if last_chunk_size < TRUNCATE_TO:
        return len(line)
    return len(line) - last_chunk_size + TRUNCATE_TO


def get_lines_info(token: tokenize.TokenInfo) -> Iterator[LineInfo]:
    if token.type not in {tokenize.COMMENT, tokenize.STRING}:
        if token.end[1] > token.start[1]:
            yield LineInfo(row=token.end[0], length=token.end[1])
        else:
            yield LineInfo(row=token.start[0], length=token.start[1])
        return

    if token.type == tokenize.COMMENT:
        # skip shebang
        if token.string.startswith('!#'):
            return
        # skip noqa, pragma, and other special tokens
        match = REX_NOQA.fullmatch(token.string)
        if match:
            return

    lines = token.string.splitlines()
    for offset, line in enumerate(lines):
        yield LineInfo(
            row=token.start[0] + offset,
            length=token.start[0] + get_line_length(line) - 1,
        )
