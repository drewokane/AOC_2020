import logging
import typing
from functools import reduce

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__, level=logging.INFO)


def parse_groups(input_data_path: str) -> typing.List[typing.List[str]]:
    raw = read_input(input_data_path).split('\n\n')
    return [group.splitlines() for group in raw]


def unanimous_answers(group_sets: typing.List[typing.List[str]]) -> typing.List[set]:
    group_answers = []

    for group in group_sets:
        logger.debug(f'Group: {group}')
        if len(group) == 1:
            group_answers.append(set(group[0]))
        else:
            group_answers.append(reduce(lambda a, b: set(a).intersection(set(b)), group[1:], group[0]))
    
    return group_answers


def main(input_data_path):
    group_sets = parse_groups(input_data_path)

    logger.debug(f'Group sets: {group_sets}')

    total = sum([len(set(''.join(g))) for g in group_sets])

    logger.info(f'Total number of yes questions: {total}')

    unanimous = unanimous_answers(group_sets)

    logger.debug(f'{unanimous}')

    total_unanimous = sum([len(g) if g else 0 for g in unanimous])

    logger.info(f'Number of unanimous yes answers: {total_unanimous}')
