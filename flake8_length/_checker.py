# built-in
import tokenize
from typing import Iterator, Sequence, Tuple

from ._parser import get_lines_info

ViolationType = Tuple[int, int, str, type]
EXCLUDED = frozenset({
    tokenize.NEWLINE,
    tokenize.ENCODING,
    tokenize.ENDMARKER,
    tokenize.ERRORTOKEN,
    tokenize.COMMA,
    tokenize.COLON,
})


class Checker:
    name = 'flake8-length'
    version = '0.0.1'

    _tokens: Sequence[tokenize.TokenInfo]

    _limit = 90
    _message = 'line is too long'

    def __init__(self, tree, file_tokens: Sequence[tokenize.TokenInfo], filename=None) -> None:
        self._tokens = file_tokens

    @classmethod
    def parse_options(cls, options) -> None:
        cls._limit = options.max_line_length

    def run(self) -> Iterator[ViolationType]:
        for token in self._tokens:
            if token.type in EXCLUDED:
                continue
            for line_info in get_lines_info(token=token):
                if line_info.length <= self._limit:
                    continue
                yield line_info.row, self._limit, self._message, type(self)
