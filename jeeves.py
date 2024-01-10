import os
from pathlib import Path

from dominate.tags import summary, details, table, thead, tr, td, tbody, code
from sh import git, pytest, tee, ErrorReturnCode


COMMENT_TEMPLATE = '''
## Test Report

{summary}

{failures}
'''


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    git.submodule.update('--remote', '--init', '--recursive')


def ci():
    """Run CI."""
    try:
        pytest('tests/test_specification.py::test_expand', color='no')
    except ErrorReturnCode as err:
        *lines, summary_line = err.stdout.decode().splitlines()

        failures = [
            line.replace('FAILED ', '').split(' - ')
            for line in sorted(lines)
            if line.startswith('FAILED')
        ]

        print(COMMENT_TEMPLATE.format(
            summary=summary_line,
            failures=details(
                summary('Test Results'),
                table(
                    thead(
                        tr(
                            td('Test'),
                            td('Error'),
                        ),
                    ),
                    tbody(
                        tr(
                            td(
                                '🔴',
                                code(test_name),
                            ),
                            td(error_text),
                        )
                        for test_name, error_text in failures
                    ),
                )
            )
        ))

        # raise ValueError(summary_line)
