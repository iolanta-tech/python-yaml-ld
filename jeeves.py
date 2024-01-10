import json
import os
from pathlib import Path

from dominate.tags import summary, details, table, thead, tr, td, tbody, code
import sh
from sh import git, pytest, tee, ErrorReturnCode

gh = sh.gh.bake(_env={**os.environ, 'NO_COLOR': '1'})


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
            line.replace('FAILED tests/', '').split(' - ')
            for line in sorted(lines)
            if line.startswith('FAILED')
        ]

        new_comment = COMMENT_TEMPLATE.format(
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
                            td(code(error_text)),
                        )
                        for test_name, error_text in failures
                    ),
                )
            )
        )

        post_new_comment = gh.pr.comment.bake(_in=new_comment)

        if pr_number := os.environ.get('PR_NUMBER'):
            post_new_comment = post_new_comment.bake(pr_number)

        post_new_comment = post_new_comment.bake(body_file='-')

        try:
            post_new_comment('--edit-last')
        except ErrorReturnCode as err:
            if 'no comments found for current user' in err.stderr.decode():
                post_new_comment()
            else:
                raise
