# built-in
from ast import AST
from tokenize import TokenInfo
from typing import Iterator, Optional, Sequence, Tuple

from flake8.options.manager import OptionManager

from ._categories import Category, Categorizer

STDIN = 'stdin'
ViolationType = Tuple[int, int, str, type]


class Checker:
    name = 'flake8-length'
    version = '0.0.1'

    _tokens: Sequence[TokenInfo]

    _categorize = Categorizer().categorize
    _limit = 90
    _message = 'line is too long'

    def __init__(
        self,
        tree: Optional[AST],
        file_tokens: Sequence[TokenInfo],
        filename: str = STDIN,
    ) -> None:
        self._tokens = file_tokens

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        option_manager.add_option(
            '--soft-line-length',
            type='int',
            metavar='n',
            default=cls._limit,
            parse_from_config=True,
            help='Maximum allowed line length for non-special cases',
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls._limit = options.soft_line_length

    def run(self) -> Iterator[ViolationType]:
        for token in self._tokens:
            cat = self._categorize(token=token)  # type: ignore
            # we validate only soft limit, hard limit is checked by pycodestyle
            if cat != Category.SOFT:
                continue
            if token.end[1] <= self._limit:
                continue
            yield token.start[0], token.start[1], self._message, type(self)
