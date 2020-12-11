import logging
import typing
from collections import defaultdict
from pprint import pformat

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__, level=logging.INFO)


def init_state_machine(raw_program: str):
    prog = raw_program.splitlines()
    return {
        'prog': prog,
        'prog_len': len(prog),
        'acc': 0,
        'position': 0,
        'loop': 0,
        'instr_count': defaultdict(int),
    }


class InstructionSet(object):

    def incr_instr_count(self, state: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        state['instr_count'][state['position']] += 1
        _, counts = zip(*state['instr_count'].items())

        if any([c == 2 for c in counts]):
            state['loop'] += 1
            logger.info(f'Looped state:\n{state}')
        return state

    def nop(self, val: str, state: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        state = self.incr_instr_count(state)
        state['position'] += 1
        return state
    
    def acc(self, val: str, state: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        state = self.incr_instr_count(state)
        state['acc'] += int(val)
        state['position'] += 1
        return state

    def jmp(self, val: str, state: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        state = self.incr_instr_count(state)
        state['position'] += int(val)
        return state


def run_machine(state: typing.Dict[str, typing.Any], inst_set: InstructionSet) -> typing.Dict[str, typing.Any]:
    if state['position'] == state['prog_len']:
        logger.info('Program terminated successfully!')
        return state

    instruction, val = state['prog'][state['position']].split()
    logger.debug(f'Instr: {instruction:<4} | Arg: {val:<5} | Pos: {state["position"]:<5}')
    return getattr(inst_set, instruction)(val, state)


def find_all_jmp_nop():
    pass


def main(data_input_path: str):
    raw = read_input(data_input_path)
    state = init_state_machine(raw)

    logger.debug(f'Initial program state:\n{state}')

    while True:
        if state['loop'] == 1:
            break

        state = run_machine(state, InstructionSet())
    
    logger.info(f'State:\n{pformat(state)}')


