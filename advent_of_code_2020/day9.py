import logging
from os import read
import typing

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__, level=logging.INFO)


def parse_input(data_path: str) -> typing.List[int]:
    return [int(n) for n in read_input(data_path).splitlines()]


def is_sum_of_past_n(target: int, n_previous: int) -> bool:
    logger.debug(f'Array: {n_previous} | Target: {target}')
    for n in n_previous:
        logger.debug(f'Candidate number: {n} | Target - Candidate = {target - n}')
        if n < target:
            if ((target - n) in n_previous) and (n != (target - n)):
                return True
    
    return False


def find_sum(target: int, array: typing.List[int]):
    start, stop = 0, 1

    while True:
        slice = array[start:stop]
        total = sum(slice)

        logger.debug(f'Star: {start} | Stop: {stop} | Array slice: {slice} | Slice sum: {total}')

        if total < target:
            stop += 1
        elif total > target:
            start += 1
            if start == stop:
                stop = start + 1
        else:
            return slice


def main(data_input_path: str):
    parsed = parse_input(data_input_path)

    preamble = 25

    for i in range(len(parsed) - preamble - 1):
        array = parsed[i:i + preamble]
        target = parsed[i + preamble]
        if not is_sum_of_past_n(target, array):
            logger.info(f'Outlier number: {target} | Position: {i + preamble}')
            break

    slice = find_sum(target, parsed)

    logger.info(f'Encryption weakness: {min(slice) + max(slice)}')
