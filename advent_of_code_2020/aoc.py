import click
import importlib

from .logging import get_logger

logger = get_logger(__name__)


@click.command()
@click.argument('day')
@click.argument('input_data_path')
def main(day, input_data_path):
    logger.info(f'Running module {day}')
    pkg = importlib.import_module(f'.{day}', package='advent_of_code_2020')
    pkg.main(input_data_path)


if __name__ == '__main__':
    main()
