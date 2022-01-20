# built-in
import tokenize
from typing import Iterator, NamedTuple, Sequence, Tuple

# app
from ._parser import get_lines_info


Tokens = Sequence[tokenize.TokenInfo]
VIOLATION_DESCRIPTION_MAP = {
    'LN001': 'code line is too long',
    'LN002': 'doc/comment line is too long'
}

TEMPLATE = '{v.code} {d} ({v.length} > {v.limit})'


class Violation(NamedTuple):
    code: str
    row: int
    length: int
    limit: int
    line: str

    def as_tuple(self) -> Tuple[int, int, str, type]:
        msg = TEMPLATE.format(v=self, d=VIOLATION_DESCRIPTION_MAP.get(self.code))
        return self.row, self.limit, msg, type(self)


class Checker:
    name = 'flake8-length'
    version = '0.0.1'
    _tokens: Tokens
    _code_limit = 90
    _doc_limit = 90

    def __init__(self, tree, file_tokens: Tokens, filename=None) -> None:
        self._tokens = file_tokens

    @classmethod
    def parse_options(cls, options) -> None:
        cls._code_limit = options.max_line_length
        cls._doc_limit = options.max_doc_length

    def run(self) -> Iterator:
        for violation in self.get_violations():
            yield violation.as_tuple()

    def get_violations(self) -> Iterator[Violation]:
        for token in self._tokens:
            for line_info in get_lines_info(token=token):
                limit = self._doc_limit if line_info.type == 'doc' else self._code_limit
                if line_info.length <= limit:
                    continue
                yield Violation(
                    code= 'LN002' if line_info.type == 'doc' else 'LN001',
                    row=line_info.row,
                    length=line_info.length,
                    limit=limit,
                    line=line_info.line,
                )
