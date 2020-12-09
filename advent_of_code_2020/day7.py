import logging
import re
import typing
from collections import defaultdict
from functools import reduce

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__, level=logging.INFO)


def reshape_child_entry(entry: str) -> typing.Optional[str]:
    if 'no other bags' in entry:
        return None
    return ' '.join(entry.replace('.', '').strip().split()[1:3])


def get_number(child: str) -> int:
    num_re = re.match(r'\d+', child)
    if num_re:
        logger.debug(f'Child entry: {child} | Number extracted: {num_re.group(0)}')
    return int(num_re.group(0) if num_re else 0)


def get_bag_type(child: str) -> str:
    return [' '.join(child.strip().split()[1:3])]


def create_child_list(entry: str) -> typing.List[str]:
    bags = entry.replace('.', '').strip().split(', ')
    bags_expanded = [get_number(b) * get_bag_type(b) for b in bags]
    logger.debug(f'Expanded bags: {bags_expanded}')
    return reduce(lambda a, b: a + b, bags_expanded, [])


def parse_bag_spec(bag_spec: str) -> typing.Dict[str, str]:
    parent, children = bag_spec.split(' bags contain ')
    logger.debug(f'Parent: {parent} | Children: {children}')
    child_dict = {reshape_child_entry(child): [parent] for child in children.split(',')}
    parent_dict = {parent: create_child_list(children)}
    logger.debug(f'Parent dictionary: {parent_dict}')
    return child_dict, parent_dict


def merge_relationships(relations: typing.List[typing.Dict[typing.Optional[str], str]]) -> typing.Dict[typing.Optional[str], typing.Set[str]]:
    combined_dict = defaultdict(list)
    for d in relations:
        logger.debug(f'Relation: {d}')
        for k, v in d.items():
            combined_dict[k].extend(v)
    
    return combined_dict


def find_lineage(child: str, relations: typing.Dict[typing.Optional[str], typing.List[str]]):
    parents = []
    next_level = relations[child]

    while next_level:
        logger.debug(f'Next level: {next_level}')
        parents = parents + next_level

        logger.debug(f'Parents: {parents}')

        next_level = reduce(lambda a, b: a + b, [relations[c] for c in next_level], [])
    
    return parents
    


def parse_rules(input_path: str) -> typing.List[str]:
    lines = read_input(input_path).splitlines()
    logger.debug(f'\n{lines}')

    bag_spec = [parse_bag_spec(spec) for spec in lines]

    return zip(*bag_spec)


def main(data_input_path: str):
    bag_relationships, parents = parse_rules(data_input_path)

    logger.debug(f'{bag_relationships}')

    combined = merge_relationships(bag_relationships)
    parents_combined = merge_relationships(parents)

    logger.debug(f'{combined}')
    logger.debug(f'Parents combined: {parents_combined}')

    lineage = find_lineage('shiny gold', combined)
    parent_lineage = find_lineage('shiny gold', parents_combined)

    logger.info(f'Number of bag colours containing shiny gold: {len(set(lineage))}')
    logger.info(f'Number of bags inside the shiny gold bag: {len(parent_lineage)}')
