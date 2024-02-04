import json
import os
import zipfile
from enum import Enum
from io import BytesIO, StringIO
from pathlib import Path
from typing import TextIO
from xml.etree import ElementTree

import funcy
import typer
from dominate.tags import summary, details, table, thead, tr, td, tbody, code
import sh
from sh import git, pytest, tee, ErrorReturnCode
from urlpath import URL

gh = sh.gh.bake(_env={**os.environ, 'NO_COLOR': '1'})


COMMENT_TEMPLATE = '''
## Test Diff Report

{body}
'''


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    git.submodule.update('--remote', '--init', '--recursive')


class TestStatus(str, Enum):
    PASSED = 'passed'
    FAILED = 'failure'
    SKIPPED = 'skipped'
    ERROR = 'error'


def _parse_pytest_xml(xml_data: TextIO):
    tree = ElementTree.parse(xml_data)
    root = tree.getroot()

    # Iterate over each testcase element
    for testcase in root.iter('testcase'):
        # Basic test information
        class_name = testcase.get('classname')
        test_name = testcase.get('name')

        full_test_name = f'{class_name}.{test_name}'

        for choice in list(TestStatus):
            if testcase.find(choice.value) is not None:
                yield full_test_name, choice
                break

        else:
            yield full_test_name, TestStatus.PASSED


def ci():
    """Run CI."""
    # Download artifact from a previous run
    previous_run = funcy.first(
        json.loads(
            gh.api('repos/iolanta-tech/python-yaml-ld/actions/artifacts'),
        )['artifacts'],
    )

    download_path = URL(previous_run['archive_download_url']).path.lstrip('/')

    previous_run_test_report = dict(
        _parse_pytest_xml(
            StringIO(
                sh.zcat(
                    _in=gh.api(download_path, _piped=True),
                ),
            ),
        ),
    )

    artifacts = Path(__file__).parent / 'tests/artifacts'
    pytest_xml = artifacts / 'pytest.xml'

    tests_success = True
    try:
        pytest.bake(
            color='no',
            junitxml=pytest_xml,
            cov_report='term-missing:skip-covered',
            cov='yaml_ld',
        ).tests(
            _out=artifacts / 'coverage.txt',
        )
    except ErrorReturnCode:
        tests_success = False

    with pytest_xml.open() as current_xml_data:
        current_test_report = dict(_parse_pytest_xml(current_xml_data))

    newly_passed = [
        test_name
        for test_name, current_result in current_test_report.items()
        if (
            current_result == TestStatus.PASSED
            and previous_run_test_report.get(test_name) != TestStatus.PASSED
        )
    ]

    newly_failed = [
        test_name
        for test_name, current_result in current_test_report.items()
        if (
            current_result in {TestStatus.FAILED, TestStatus.ERROR}
            and previous_run_test_report.get(test_name) == TestStatus.PASSED
        )
    ]

    comment_body_parts = []
    if newly_passed:
        comment_body_parts.append('## Newly passed!')

        for test_name in newly_passed:
            comment_body_parts.append(f'* {test_name}')

    if newly_failed:
        comment_body_parts.append('## Newly failed :(((')

        for test_name in newly_failed:
            comment_body_parts.append(f'* {test_name}')

    if not comment_body_parts:
        comment_body_parts.append('Nothing had changed.')

    comment = COMMENT_TEMPLATE.format(
        body='\n\n'.join(comment_body_parts),
    )

    post_new_comment = gh.pr.comment.bake(_in=comment)

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

    if not tests_success:
        raise typer.Exit(1)

    """
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
    """
