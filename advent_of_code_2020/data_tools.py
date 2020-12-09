import typing


def read_input(input_path: str) -> str:
    with open(input_path, 'r') as f:
        data = f.read()
    return data


def parse_records(input_path: str) -> typing.List[str]:
    return read_input(input_path).split('\n\n')


def load_string_array(input_path: str, sep: typing.Optional[str] = None) -> typing.List[typing.Any]:
    raw_data = read_input(input_path).splitlines()

    if sep:
        out = [l.split(sep) for l in raw_data]
    else:
        out = [list(l) for l in raw_data]

    return out
