# built-in
import tokenize
from typing import Iterator, NamedTuple, Sequence, Tuple

# app
from ._parser import get_lines_info


Tokens = Sequence[tokenize.TokenInfo]
TEMPLATE = 'LN001 line is too long ({v.length} > {v.limit})'


class Violation(NamedTuple):
    row: int
    length: int
    limit: int
    line: str

    def as_tuple(self) -> Tuple[int, int, str, type]:
        msg = TEMPLATE.format(v=self)
        return self.row, self.limit, msg, type(self)


class Checker:
    name = 'flake8-length'
    version = '0.0.1'
    _tokens: Tokens
    _limit = 90

    def __init__(self, tree, file_tokens: Tokens, filename=None) -> None:
        self._tokens = file_tokens

    @classmethod
    def parse_options(cls, options) -> None:
        cls._limit = options.max_line_length

    def run(self) -> Iterator:
        for violation in self.get_violations():
            yield violation.as_tuple()

    def get_violations(self) -> Iterator[Violation]:
        for token in self._tokens:
            for line_info in get_lines_info(token=token):
                if line_info.length <= self._limit:
                    continue
                yield Violation(
                    row=line_info.row,
                    length=line_info.length,
                    limit=self._limit,
                    line=line_info.line,
                )
