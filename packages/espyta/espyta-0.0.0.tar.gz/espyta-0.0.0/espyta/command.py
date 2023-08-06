"""Collection of espyta's command line entry points that allow you to start
a HTTP server."""

import sys
import logging

from datetime import datetime, timedelta

from typing import Optional

import click

import tornado.ioloop


log = logging.getLogger(__name__)


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Verbosity, passing more heightens the verbosity.",
)
@click.option("--configuration-path", default=None, help="Configuration file.")
def main(verbose: int, configuration_path: Optional[str]) -> None:
    """espyta ESP OTA manager."""
    logging.basicConfig(level=10 + (logging.FATAL - verbose * 10))

    from espyta import configuration

    if configuration_path:
        import toml

        with open(configuration_path) as file:
            configuration_file = toml.load(file)

            for key, value in configuration_file.items():
                setattr(configuration, key, value)


@main.command()
@click.option("--port", default=8000, help="Port to listen to.")
def http(port: int) -> None:
    """Run espyta's HTTP server."""
    from espyta.http import make_application

    application = make_application()
    application.listen(port, xheaders=True)
    tornado.ioloop.IOLoop.current().start()
