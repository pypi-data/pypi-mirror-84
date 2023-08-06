import click

import logging
import klogs


@click.group()
def main():
    pass


@main.command()
def hello():
    klogs.configure_logging()
    logging.getLogger().info("Hello, world!")


if __name__ == "__main__":
    main()
