import click

import logging
import clogs


@click.group()
def main():
    pass


@main.command()
def hello():
    logga.configure_logging()
    logging.getLogger().info("Hello, world!")


if __name__ == "__main__":
    main()
