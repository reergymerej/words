#!/usr/bin/env python

import argparse


import logging
import os
import re
from sys import argv
from typing import List, Tuple

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(message)s")

from pathlib import Path


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description='Count words in your dirty little files'
    )
    parser.add_argument(
            'input_file_path',
            help='path to file you want counted',
            type=Path,
    )
    parser.add_argument(
            '--sort',
            help='sort output by count or by word',
            choices=['count', 'word'],
            default='count',
    )
    return parser.parse_args(args)


def convert_dict(counts: dict, sort_by: str) -> List[Tuple]:
    totals = []
    for word, count in counts.items():
        logging.debug(f'word: {word}, count: {count}')
        totals.append((count, word))
    logging.debug(f'sorting by {sort_by}')
    if sort_by == 'count':
        return sorted([
            (count, word) for word, count in counts.items()
        ], reverse=True)
    else:
        return [
            (count, word) for word, count in sorted([
                (word, count) for word, count in counts.items()
            ])
        ]


def main(args: List[str]):
    arg_parser = parse_args(args)

    input_file_path = Path(arg_parser.input_file_path)
    logging.debug(f'counting words in {input_file_path}')

    counts = {}
    pattern = r'[a-zA-Z]+'

    with open(input_file_path) as f:
        lines_processed = 0
        while True:
            try:
                line = f.readline()
                if not line:
                    break
                logging.debug(f'line # {lines_processed + 1}')

                for x in re.finditer(pattern, line):
                    word = x.group(0).lower()
                    if word in counts:
                        counts[word] = counts[word] + 1
                    else:
                        counts[word] = 1
                    logging.debug(f'{word}: {counts[word]}')

                lines_processed = lines_processed + 1
            except Exception as e:
                logging.error(e)



        totals = convert_dict(counts, sort_by=arg_parser.sort)

        for count, word in totals:
            print(f'{count}\t{word}')



if __name__ == '__main__':
    main(argv[1:])
