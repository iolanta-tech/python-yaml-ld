import functools
import json
import logging
import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Optional

import funcy
import yaml
from documented import Documented
from rich.console import Console
from rich.errors import NotRenderableError
from rich.panel import Panel
from rich.syntax import Syntax
from typer import Argument, Option, Typer
from yarl import URL

import yaml_ld
from yaml_ld.compact import CompactOptions
from yaml_ld.document_loaders.default import CACHE_DIRECTORY
from yaml_ld.expand import ExpandOptions
from yaml_ld.flatten import FlattenOptions
from yaml_ld.from_rdf import FromRDFOptions
from yaml_ld.models import JsonLdRecord
from yaml_ld.to_rdf import ToRDFOptions

cli = Typer(
    no_args_is_help=True,
    help=(
        'Command line tool to operate on ＊-LD data, '
        'where ＊ stands for JSON or YAML.'
    ),
)
console = Console()


MaybeStr = Optional[str]


class LogLevel(StrEnum):
    """Logging level for the application."""

    DEBUG = 'debug'
    INFO = 'info'     # noqa: WPS110
    ERROR = 'error'


@cli.callback()
def _root_app_callback(  # noqa: WPS430
    log_level: Annotated[
        LogLevel, Option(help='Logging level.'),
    ] = LogLevel.ERROR,
):  # pragma: nocover
    cli.log_level = log_level   # type: ignore
    logging.basicConfig(
        level={
            LogLevel.ERROR: logging.ERROR,
            LogLevel.INFO: logging.INFO,
            LogLevel.DEBUG: logging.DEBUG,
        }[log_level],
    )


def decode_input(input_: str | None) -> Path | URL:
    """Interpret the input as location of the document."""
    match input_:
        case None:
            return Path('/dev/stdin')

        case str() as string:
            url = URL(string)

            if url.scheme:
                return url

            return Path(string)


class OutputFormat(StrEnum):
    """Output format."""

    JSON = 'json'
    YAML = 'yaml'


class RDFFormat(StrEnum):
    """Output format."""

    NQUADS = 'nquads'


def pretty_print(
    document: JsonLdRecord | list[JsonLdRecord],
    output_format: OutputFormat | RDFFormat,
) -> Syntax:
    """Serialize an LD document."""
    serializer = {
        OutputFormat.JSON: functools.partial(json.dumps, indent=2, default=str),
        OutputFormat.YAML: functools.partial(yaml.dump, Dumper=yaml.SafeDumper),
        RDFFormat.NQUADS: funcy.identity,
    }[output_format]

    serialized_document = serializer(document)

    return Syntax(
        serialized_document,
        lexer=output_format.value,
        background_color='default',
    )


@cli.command()
@funcy.post_processing(console.print)
def expand(
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    output_format: Annotated[
        OutputFormat,
        Option(help='Format to output the data at.'),
    ] = OutputFormat.JSON,
    base: Annotated[MaybeStr, Option(help='Base URL.')] = None,
    extract_all_scripts: Annotated[
        bool,
        Option(
            help=(
                'Extract all documents in YAML stream, or all scripts '
                'embedded in HTML.'
            ),
        ),
    ] = False,
    expand_context: Annotated[
        MaybeStr,
        Option(help='Context to expand with.'),
    ] = None,
):
    """Expand a ＊-LD document."""
    response = yaml_ld.expand(
        document=decode_input(input_),
        options=ExpandOptions(
            base=base,
            extract_all_scripts=extract_all_scripts,
            expand_context=expand_context,
        ),
    )

    return pretty_print(
        document=response,
        output_format=output_format,
    )


@cli.command()
@funcy.post_processing(console.print)
def get(
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    base: Annotated[MaybeStr, Option(help='Base URL.')] = None,
    output_format: Annotated[
        OutputFormat,
        Option(help='Format to output the data at.'),
    ] = OutputFormat.JSON,
):
    """Load and display a ＊-LD document."""
    response = yaml_ld.load_document(
        decode_input(input_),
        base=base,
    )['document']

    return pretty_print(
        document=response,
        output_format=output_format,
    )


@cli.command()
@funcy.post_processing(console.print)
def compact(   # noqa: WPS211
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    ctx: Annotated[
        MaybeStr,
        Option(help='Context to compact with.'),
    ] = None,
    output_format: Annotated[
        OutputFormat,
        Option(help='Format to output the data at.'),
    ] = OutputFormat.JSON,
    base: Annotated[MaybeStr, Option(help='Base URL.')] = None,
    extract_all_scripts: Annotated[
        bool,
        Option(
            help=(
                'Extract all documents in YAML stream, or all scripts '
                'embedded in HTML.'
            ),
        ),
    ] = True,
    expand_context: Annotated[
        MaybeStr,
        Option(help='Context to expand with.'),
    ] = None,
):
    """Compact a ＊-LD document."""
    response = yaml_ld.compact(
        document=decode_input(input_),
        ctx=ctx or {},
        options=CompactOptions(
            base=base,
            extract_all_scripts=extract_all_scripts,
            expand_context=expand_context,
        ),
    )

    return pretty_print(
        document=response,
        output_format=output_format,
    )


@cli.command()
@funcy.post_processing(console.print)
def flatten(    # noqa: WPS211
    ctx: Annotated[
        MaybeStr,
        Option(help='Context to compact with.'),
    ] = None,
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    output_format: Annotated[
        OutputFormat,
        Option(help='Format to output the data at.'),
    ] = OutputFormat.JSON,
    base: Annotated[MaybeStr, Option(help='Base URL.')] = None,
    extract_all_scripts: Annotated[
        bool,
        Option(
            help=(
                'Extract all documents in YAML stream, or all scripts '
                'embedded in HTML.'
            ),
        ),
    ] = True,
    expand_context: Annotated[
        MaybeStr,
        Option(help='Context to expand with.'),
    ] = None,
):
    """Flatten a ＊-LD document."""
    response = yaml_ld.flatten(
        document=decode_input(input_),
        ctx=ctx,
        options=FlattenOptions(
            base=base,
            extract_all_scripts=extract_all_scripts,
            expand_context=expand_context,
        ),
    )

    return pretty_print(
        document=response,
        output_format=output_format,
    )


@cli.command()
@funcy.post_processing(console.print)
def to_rdf(
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    output_format: Annotated[
        RDFFormat,
        Option(help='Format to output the data at.'),
    ] = RDFFormat.NQUADS,
    base: Annotated[MaybeStr, Option(help='Base URL.')] = None,
    extract_all_scripts: Annotated[
        bool,
        Option(
            help=(
                'Extract all documents in YAML stream, or all scripts '
                'embedded in HTML.'
            ),
        ),
    ] = True,
):
    """Convert a ＊-LD document → RDF."""
    return yaml_ld.to_rdf(
        document=decode_input(input_),
        options=ToRDFOptions(
            base=base,
            format='application/n-quads',
            extract_all_scripts=extract_all_scripts,
        ),
    )


@cli.command()
@funcy.post_processing(console.print)
def from_rdf(
    input_: Annotated[
        MaybeStr,
        Argument(help='Path or URL. Omit to read from standard input.'),
    ] = None,
    output_format: Annotated[
        OutputFormat,
        Option(help='Format to output the data at.'),
    ] = OutputFormat.JSON,
):
    """Convert an RDF document → ＊-LD form."""
    response = yaml_ld.from_rdf(
        dataset=str(decode_input(input_)),
        options=FromRDFOptions(),
    )

    return pretty_print(
        document=response,
        output_format=output_format,
    )


cache = Typer(help='Cache management.', no_args_is_help=True)
cli.add_typer(cache, name='cache')


@cache.command()
def clear():
    """Clear cache."""
    shutil.rmtree(CACHE_DIRECTORY)
    console.print('Cache cleared.', style='green')


@dataclass
class FormattedError(Documented):   # type: ignore
    """**{self.exception_class}:** {self.message}"""  # noqa: D400

    exception: Exception

    @property
    def exception_class(self):
        """Class of the exception."""
        return self.exception.__class__.__name__

    @property
    def message(self):
        """Exception message."""
        return str(self.exception)


def print_unhandled_exception(err: Exception):  # pragma: no cover
    """Print unhandled exception as an error message."""
    try:
        console.print(Panel(err, style='red'))  # type: ignore
    except NotRenderableError:
        console.print(Panel(FormattedError(exception=err), style='red'))

    console.print(TracebackAdvice())


class TracebackAdvice(Documented):  # pragma: no cover
    """
    💡 To see Python traceback, use:

    `pyld --log-level info {self.args}`
    """  # noqa: D400

    @property
    def args(self):
        """Format current CLI args."""
        return ' '.join(funcy.rest(sys.argv))


def app() -> None:    # pragma: no cover
    """Construct and return Typer app."""
    try:
        return cli()

    except Exception as err:
        if cli.log_level == LogLevel.ERROR:    # type: ignore
            print_unhandled_exception(err)
            sys.exit(1)

        else:
            raise
