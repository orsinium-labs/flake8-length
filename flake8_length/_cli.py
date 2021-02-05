# built-in
import sys
import tokenize
from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence, TextIO

# app
from ._checker import Checker


TEMPLATE = "{path}:{vl.row}: {vl.length} > {vl.limit}"


def main(argv: Sequence[str], stream: TextIO = sys.stdout) -> int:
    parser = ArgumentParser()
    parser.add_argument('--max', type=int, default=90)
    parser.add_argument('--show', action='store_true')
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args(argv)

    violations = 0
    for path in args.paths:
        with path.open('rb') as file_stream:
            tokens = list(tokenize.tokenize(file_stream.__next__))
            checker = Checker(None, tokens)
            checker._limit = args.max
            for vl in checker.get_violations():
                violations += 1
                msg = TEMPLATE.format(path=path, vl=vl)
                print(msg, file=stream)
                if args.show:
                    print(' ', vl.line.strip(), file=stream)
    return violations


def entrypoint():
    sys.exit(main(argv=sys.argv[1:]))
