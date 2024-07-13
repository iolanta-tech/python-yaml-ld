"""MkDocs macros for the documentation site."""
import functools
from pathlib import Path
from typing import List, Optional

import sh
from mkdocs_macros.plugin import MacrosPlugin

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


def define_env(env: MacrosPlugin):
    """Register macros."""
    env.macro(
        functools.partial(
            run_python_script,
            docs_dir=Path(env.conf['docs_dir']),
        ),
        name='run_python_script',
    )
