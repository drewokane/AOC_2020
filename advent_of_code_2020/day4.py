import re
from collections import namedtuple
import typing

from .data_tools import read_input
from .logging import get_logger

logger = get_logger(__name__)

Passport = namedtuple(
    'Passport',
    ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'],
    
)
DefaultPassport = Passport(None, None, None, None, None, None, None, None)


def parse_records(raw_data: str):
    lines = re.split(r'\n\n', raw_data)
    return [marshal_passport(l) for l in lines]


def marshal_passport(passport_str: str) -> Passport:
    fields = passport_str.split()
    passport_dict = {f.split(':')[0]: f.split(':')[1] for f in fields}
    return DefaultPassport._replace(**passport_dict)


def maybe_parse_int(num: str) -> int:
    try:
        out = int(num)
    except:
        out = -1
    finally:
        return out


def validate_passport(passport: Passport) -> bool:
    fields = sum([1 if v else 0 for _, v in passport._asdict().items()])
    if passport.cid:
        if fields != 8:
            logger.debug('Not enough fields!')
            return False
    else:
        if fields != 7:
            logger.debug('Not enough fields!')
            return False

    if not (1920 <= maybe_parse_int(passport.byr) <= 2002):
        logger.debug(f'Invalid birth year: {passport.byr}')
        return False
    
    if not (2010 <= maybe_parse_int(passport.iyr) <= 2020):
        logger.debug(f'Invalid issue year: {passport.iyr}')
        return False
    
    if not (2020 <= maybe_parse_int(passport.eyr) <= 2030):
        logger.debug(f'Invalid expiration year: {passport.eyr}')
        return False
    
    unit = passport.hgt[-2:]
    if not (unit in ['cm', 'in']):
        logger.debug(f'Invalid unit: {unit}')
        return False
    else:
        hgt = maybe_parse_int(passport.hgt[:-2])
        if unit == 'cm':
            if not (150 <= hgt <= 193):
                logger.debug(f'Invalid cm height: {hgt}')
                return False
        if unit == 'in':
            if not (59 <= hgt <= 76):
                logger.debug(f'Invalid inch height: {hgt}')
                return False
    
    if not (passport.hcl[0] == '#'):
        logger.debug(f'Invalid hex color, no beginning hash: {passport.hcl}')
        return False
    elif not (len(passport.hcl[1:]) == 6):
        logger.debug(f'Hair color hex wrong length: {passport.hcl}')
        return False
    elif re.match('[g-z]', passport.hcl[1:]):
        logger.debug(f'Invalid hair color: {passport.hcl}')
        return False
    
    valid_ecl = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
    if not (passport.ecl in valid_ecl):
        logger.debug(f'Invalid eye color: {passport.ecl}')
        return False
    
    if not (len(passport.pid) == 9):
        logger.debug(f'Passport ID wrong length: {passport.pid}')
        return False
    elif not (maybe_parse_int(passport.pid) >= 0):
        logger.debug(f'Invalid passport ID characters: {passport.pid}')
        return False
    
    return True    


def filter_valid_records(records: typing.List[Passport]) -> typing.List[Passport]:
    filtered = []
    for rec in records:
        if validate_passport(rec):
            filtered.append(rec)
    
    return filtered

def main(input_data_path):
    raw = read_input(input_data_path)
    parsed = parse_records(raw)
    filtered = filter_valid_records(parsed)

    logger.info(f'Number of records: {len(parsed)}')
    logger.info(f'Number of valid records: {len(filtered)}')    
