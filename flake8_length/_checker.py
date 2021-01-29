# built-in
import enum
import re
import tokenize as tokens
from ast import AST
from tokenize import TokenInfo
from typing import Iterator, Optional, Sequence, Tuple

STDIN = 'stdin'
ViolationType = Tuple[int, int, str, type]


class Category(enum.Enum):
    EXCLUDED = enum.auto()
    SOFT = enum.auto()
    HARD = enum.auto()


class Categorizer:
    _excluded = frozenset({
        tokens.NEWLINE,
        tokens.ENCODING,
        tokens.ENDMARKER,
    })
    _texts = frozenset({
        tokens.STRING,
        tokens.COMMENT,
    })
    _rex_url = re.compile(r'[a-z]://.+')
    _rex_noqa = re.compile(r'(noqa|[nwer]:|pragma).+')
    _rex_str = re.compile(r'[fbru](?:\'|"|\'\'\'|""")(.*)(?:\'|"|\'\'\'|""")')

    def categorize(self, token: TokenInfo) -> Category:
        if token.type in self._excluded:
            return Category.EXCLUDED
        content = self.get_content(token=token)
        if content is None:
            return Category.HARD

        if token.type == tokens.COMMENT:
            if self.is_url(content=content):
                return Category.SOFT
            if self.is_noqa(content=content):
                return Category.SOFT

        if token.type == tokens.STRING:
            if len(content) < 5:
                return Category.HARD
            return Category.SOFT

        return Category.HARD

    def get_content(self, token: TokenInfo) -> Optional[str]:
        if token.type not in self._texts:
            return None
        content = token.string
        if token.type == tokens.COMMENT:
            return content[1:].lstrip()

        if token.type != tokens.STRING:
            return content
        match = self._rex_str.fullmatch(content)
        if not match:
            return content
        return match.group(1)

    def is_url(self, content: str) -> bool:
        content = content.lower().strip()
        match = self._rex_url.fullmatch(content)
        return bool(match)

    def is_noqa(self, content: str) -> bool:
        content = content.lower().strip()
        match = self._rex_noqa.fullmatch(content)
        return bool(match)


class Checker:
    name = 'flake8-length'
    version = '0.0.1'

    _tokens: Sequence[TokenInfo]

    _categorize = Categorizer().categorize
    _limit = 90
    _message = 'line is too long'

    def __init__(self, tree: AST, file_tokens: Sequence[TokenInfo], filename: str = STDIN) -> None:
        self._tokens = file_tokens

    def run(self) -> Iterator[ViolationType]:
        for token in self._tokens:
            cat = self._categorize(token=token)  # type: ignore
            # we validate only soft limit, hard limit is checked by pycodestyle
            if cat != Category.SOFT:
                continue
            if token.end[1] <= self._limit:
                continue
            yield token.start[0], token.start[1], self._message, type(self)
