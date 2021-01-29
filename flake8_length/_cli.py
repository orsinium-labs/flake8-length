import sys
import tokenize
from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence, TextIO

from ._checker import Checker

TEMPLATE = "{path}:{row}"


def main(argv: Sequence[str], stream: TextIO = sys.stdout) -> int:
    parser = ArgumentParser()
    parser.add_argument('--max', type=int)
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args(argv)

    violations = 0
    for path in args.paths:
        with path.open('rb') as file_stream:
            tokens = list(tokenize.tokenize(file_stream.__next__))
            checker = Checker(None, tokens)
            for violation in checker.run():
                violations += 1
                msg = TEMPLATE.format(
                    path=path,
                    row=violation[0],
                )
                print(msg, file=stream)
    return violations


def entrypoint():
    sys.exit(main(argv=sys.argv[1:]))
