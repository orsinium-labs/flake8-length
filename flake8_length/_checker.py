# built-in
import tokenize
from typing import Iterator, NamedTuple, Sequence, Tuple

# app
from ._parser import get_lines_info, Message


Tokens = Sequence[tokenize.TokenInfo]
TEMPLATE = '{v.code} {v.message.value} ({v.length} > {v.limit})'


class Violation(NamedTuple):
    message: Message
    row: int
    length: int
    limit: int
    line: str

    @property
    def code(self) -> str:
        return self.message.name

    def as_tuple(self) -> Tuple[int, int, str]:
        msg = TEMPLATE.format(v=self)
        return self.row, self.limit, msg


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
        if options.max_doc_length:
            cls._doc_limit = options.max_doc_length
        else:
            cls._doc_limit = options.max_line_length

    def run(self) -> Iterator[tuple]:
        for violation in self.get_violations():
            yield violation.as_tuple() + (type(self),)

    def get_violations(self) -> Iterator[Violation]:
        for token in self._tokens:
            for line_info in get_lines_info(token=token):
                if line_info.message == Message.LN002:
                    limit = self._doc_limit
                else:
                    limit = self._code_limit
                if line_info.length <= limit:
                    continue
                yield Violation(
                    message=line_info.message,
                    row=line_info.row,
                    length=line_info.length,
                    limit=limit,
                    line=line_info.line,
                )
