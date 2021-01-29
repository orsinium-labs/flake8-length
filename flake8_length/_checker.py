# built-in
import tokenize
from typing import Iterator, Sequence, Tuple

from ._parser import get_lines_info

Violation = Tuple[int, int, str, type]
Tokens = Sequence[tokenize.TokenInfo]


class Checker:
    name = 'flake8-length'
    version = '0.0.1'

    _tokens: Tokens

    _limit = 90
    _message = 'line is too long'

    def __init__(self, tree, file_tokens: Tokens, filename=None) -> None:
        self._tokens = file_tokens

    @classmethod
    def parse_options(cls, options) -> None:
        cls._limit = options.max_line_length

    def run(self) -> Iterator[Violation]:
        for token in self._tokens:
            for line_info in get_lines_info(token=token):
                if line_info.length <= self._limit:
                    continue
                yield line_info.row, self._limit, self._message, type(self)
