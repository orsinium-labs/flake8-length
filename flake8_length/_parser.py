# built-in
import tokenize
from typing import Iterator, NamedTuple


SKIP_PREFIXES = ('noqa', 'n:', 'w:', 'e:', 'r:', 'pragma:')
SQL_PREFIXES = ('SELECT ', 'UPDATE', 'DELETE ')
TRUNCATE_TO = 10
EXCLUDED = frozenset({
    tokenize.NEWLINE,
    tokenize.NL,
    tokenize.ENCODING,
    tokenize.ENDMARKER,
    tokenize.ERRORTOKEN,
    tokenize.COMMA,
    tokenize.RBRACE,
    tokenize.COLON,
})


class LineInfo(NamedTuple):
    row: int
    length: int
    line: str


def get_line_length(line: str) -> int:
    chunks = line.split()
    if not chunks:
        return len(line)
    last_chunk_size = len(chunks[-1])
    if last_chunk_size < TRUNCATE_TO:
        return len(line)
    return len(line) - last_chunk_size + TRUNCATE_TO


def get_lines_info(token: tokenize.TokenInfo) -> Iterator[LineInfo]:
    if token.type in EXCLUDED:
        return

    if token.type not in {tokenize.COMMENT, tokenize.STRING}:
        if token.end[1] > token.start[1]:
            yield LineInfo(row=token.end[0], length=token.end[1], line=token.line)
        else:
            yield LineInfo(row=token.start[0], length=token.start[1], line=token.line)
        return

    if token.type == tokenize.COMMENT:
        # skip shebang
        if token.string.startswith('#!'):
            return
        # skip noqa, pragma, and other special tokens
        if token.string.lower()[1:].lstrip().startswith(SKIP_PREFIXES):
            return

    # skip single-line strings
    if token.type == tokenize.STRING and '\n' not in token.string:
        # do not skip SQL queries
        if token.string.lstrip('brfu').lstrip('"\'').startswith(SQL_PREFIXES):
            yield LineInfo(
                row=token.start[0],
                length=token.start[1] + get_line_length(token.string),
                line=token.line,
            )
        return

    # analyze every line of comments and multiline strings
    lines = token.string.splitlines()
    for offset, line in enumerate(lines):
        yield LineInfo(
            row=token.start[0] + offset,
            length=token.start[1] + get_line_length(line),
            line=line,
        )
