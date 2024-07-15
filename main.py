"""MkDocs macros for the documentation site."""
import os
import functools
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Any

import sh
from mkdocs_macros.plugin import MacrosPlugin

import yaml_ld
from yaml_ld import cli   # noqa: WPS458


TERMINAL_TEMPLATE = """
```{language} title="↦ <code>{title}</code>"
{output}
```
"""

STDERR_TEMPLATE = """
!!! danger "Error"
    ```
{stderr}
    ```
"""


PYTHON_TEMPLATE = """
```python title="{cmd} {path.name}"
{stdout}
```

{stderr}
"""


JEEVES_TEMPLATE = """
``` title="↦ <code>{cmd}</code>"
{stdout}
```

{stderr}
"""


@dataclass
class FunctionDescription:
    """Description of a python-yaml-ld operation."""

    function: Any   # type: ignore
    cli: Any   # type: ignore
    icon: str

    @property
    def function_name(self) -> str:
        """Function name."""
        return self.function.__name__

    @property
    def function_docstring(self) -> str:
        """Function description."""
        return self.function.__doc__.strip().splitlines()[0]

    @property
    def function_url(self) -> str:
        """Function doc page."""
        return self.function_name.replace('_', '-')

    @property
    def command_name(self) -> str:
        """CLI command name."""
        return self.cli.__name__.replace('_', '-')

    @property
    def command_url(self) -> str:
        """URL for command page."""
        return self.command_name


def format_annotations(annotations: List[str]) -> str:
    """Format annotations for mkdocs-material to accept them."""
    enumerated_annotations = enumerate(annotations, start=1)

    return '\n\n'.join(
        f'{number}. {annotation}'
        for number, annotation in enumerated_annotations
    )


def run_python_script(   # noqa: WPS210
    path: str,
    docs_dir: Path,
    annotations: Optional[List[str]] = None,
    args: Optional[List[str]] = None,
):
    """Run a given Python file, embed results into docs."""
    if annotations is None:
        annotations = []

    if args is None:
        args = []

    code_path = docs_dir / path
    code = code_path.read_text()

    stderr = None
    try:
        stdout = sh.python(
            *args,
            code_path,
            retcode=None,
            _cwd=code_path.parent,
        )
    except sh.ErrorReturnCode as error_return_code:
        stdout = error_return_code.stdout
        stderr = error_return_code.stdout

    cmd = 'python'
    if args:
        formatted_args = ' '.join(args)
        cmd = f'{cmd} {formatted_args}'

    return PYTHON_TEMPLATE.format(
        path=code_path,
        code=code,
        stdout=stdout,
        stderr=stderr or '',
        annotations=format_annotations(annotations),
        cmd=cmd,
    )


def formatted_stderr(stderr: Optional[str]) -> str:
    """Format the std err."""
    if not stderr:
        return ''

    return STDERR_TEMPLATE.format(stderr=stderr)


def terminal(
    command: str,
    title: Optional[str] = None,
    cwd: Optional[str] = None,
    language: str | None = None,
):
    """Run command and print its output."""
    execute = sh.bash.bake(
        '-c',
        _env={**os.environ},
        _tty_out=False,
    )

    if cwd:
        execute = execute.bake(_cwd=cwd)

    output = execute(command)

    return TERMINAL_TEMPLATE.format(
        output=output,
        title=title or command,
        language=language or '',
    )


def define_env(env: MacrosPlugin):
    """Register macros."""
    env.macro(
        functools.partial(
            run_python_script,
            docs_dir=Path(env.conf['docs_dir']),
        ),
        name='run_python_script',
    )

    env.macro(
        terminal,
        name='terminal',
    )

    env.variables['functions'] = [
        FunctionDescription(
            function=yaml_ld.load_document,
            cli=cli.get,
            icon='fontawesome-solid-explosion',
        ),
        FunctionDescription(
            function=yaml_ld.expand,
            cli=cli.expand,
            icon='fontawesome-solid-explosion',
        ),
        FunctionDescription(
            function=yaml_ld.compact,
            cli=cli.compact,
            icon='compression',
        ),
        FunctionDescription(
            function=yaml_ld.flatten,
            cli=cli.flatten,
            icon='material-train-car-flatbed',
        ),
        FunctionDescription(
            function=yaml_ld.to_rdf,
            cli=cli.to_rdf,
            icon='material-graph',
        ),
        FunctionDescription(
            function=yaml_ld.from_rdf,
            cli=cli.from_rdf,
            icon='material-graph',
        ),
        FunctionDescription(
            function=yaml_ld.frame,
            cli=None,
            icon='material-image-frame',
        ),
    ]
