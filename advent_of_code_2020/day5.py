import logging
import typing

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__)


def parse_tickets(data_path: str) -> typing.List[str]:
    return read_input(data_path).splitlines()


def generate_row_number(ticket: str) -> int:
    low, high = 0, 127
    row = 0

    logger.debug(f'Ticket: {ticket}')

    for i in range(7):
        letter = ticket[i]
        width = high - low + 1

        logger.debug(f'Ticket seq[{i}] = {letter}')

        if letter == 'F':
            high = high - (width // 2)
            row = low
        elif letter == 'B':
            low = low + (width // 2)
            row = high
        
        logger.debug(f'Row = {row} | Low = {low} | High = {high}')
    
    return row


def generate_column_number(ticket: str) -> int:
    low, high = 0, 7
    col = 0

    logger.debug(f'Ticket: {ticket}')

    for i in range(7, 10):
        letter = ticket[i]
        width = high - low + 1

        logger.debug(f'Ticket seq[{i}] = {letter}')

        if letter == 'L':
            high = high - (width // 2)
            col = low
        elif letter == 'R':
            low = low + (width // 2)
            col = high
        
        logger.debug(f'Column = {col} | Low = {low} | High = {high}')
    
    return col


def generate_seat_ids(tickets: typing.List[str]) -> typing.List[int]:
    seat_ids = []
    
    for ticket in tickets:
        row = generate_row_number(ticket)
        col = generate_column_number(ticket)
        seat_ids.append((8 * row) + col)
    
    return sorted(seat_ids)


def find_gap(seat_ids: typing.List[int]) -> int:
    for i in range(len(seat_ids) - 1):
        diff = seat_ids[i + 1] - seat_ids[i]
        if diff > 1:
            return seat_ids[i] + 1


def main(input_data_path: str):
    tickets = parse_tickets(input_data_path)

    logger.debug(f'Tickets:\n{tickets}')

    seat_ids = generate_seat_ids(tickets)

    logger.info(f'Maximum seat ID: {max(seat_ids)}')

    missing_id = find_gap(seat_ids)

    logger.info(f'Missing seat ID: {missing_id}')
