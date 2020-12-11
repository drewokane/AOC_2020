import logging
import typing
from collections import Counter
from functools import reduce
from math import factorial
from operator import mul

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__, level=logging.DEBUG)


def diff_jolts(joltages: typing.List[int]):
    low, high = joltages[:-1], joltages[1:]
    return [joltages[0]] + [h - l for h, l in zip(high, low)] + [3]


def combinations(d: int) -> int:
    combos = {
        0: 1,
        1: 1,
        2: 2,
        3: 4,
        4: 7,
    }
    return combos[d]


def get_1_diffs(diffs: typing.List[int]) -> typing.List[str]:
    one_diffs = ''.join([str(d) for d in diffs]).split('3')
    lengths = [len(d) for d in one_diffs]
    logger.debug(f'Counts: {Counter(lengths)}')
    return [combinations(l) for l in lengths]


def calc_valid_sequences(diffs: typing.List[int]) -> int:
    combos = get_1_diffs(diffs)
    logger.debug(f'Number of combinations for each 1-diff seq:\n{combos}')
    return reduce(mul, combos)


def main(input_data_path: str):
    jolt_adaptors = sorted([int(n) for n in read_input(input_data_path).splitlines()])
    logger.debug(f'Adaptors:\n{jolt_adaptors}')

    differences = diff_jolts(jolt_adaptors)
    logger.debug(f'Differences:\n{differences}')

    counts = Counter(differences)
    logger.debug(f'1-diffs: {counts[1]} | 2-diffs: {counts[2]} | 3-diffs: {counts[3]}')

    logger.info(f'1-diffs * 3-diffs = {counts[1] * counts[3]}')

    num_seqs = calc_valid_sequences(differences)
    logger.info(f'Number of valid joltage sequences: {num_seqs}')
