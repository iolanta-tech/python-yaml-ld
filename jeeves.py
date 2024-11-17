import json
import os
from enum import Enum, StrEnum, auto
from io import StringIO
from pathlib import Path
from typing import TextIO
from xml.etree import ElementTree  # noqa: S405

import funcy
import rich
import sh
import typer
from pyld import jsonld
from yarl import URL

import yaml_ld

COMMENTING_NOT_ALLOWED = (
    'GraphQL: Resource not accessible by integration (addComment)'
)

gh = sh.gh.bake(_env={**os.environ, 'NO_COLOR': '1'})

artifacts = Path(__file__).parent / 'tests/artifacts'
pytest_xml = artifacts / 'pytest.xml'


COMMENT_TEMPLATE = '''
## Test Diff Report

{body}
'''


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    sh.git.submodule.update('--remote', '--init', '--recursive')


class TestStatus(StrEnum):
    """Status of a unit test."""

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


def test_with_artifacts():
    """Run pytest and save the results to artifacts directory."""
    try:
        sh.pytest.bake(
            color='no',
            junitxml=pytest_xml,
            cov_report='term-missing:skip-covered',
            cov='yaml_ld',
        ).tests(
            _out=artifacts / 'coverage.txt',
        )
    except sh.ErrorReturnCode as err:
        typer.echo(err)
        typer.echo(err.stdout)
        typer.echo(err.stderr)


class PostComment(Enum):
    """Status of a comment post attempt."""

    POSTED = auto()
    NO_EXISTING_COMMENTS = auto()
    NOT_ALLOWED = auto()


def _post(command):
    try:
        command()
    except sh.ErrorReturnCode as err:
        error_text = err.stderr.decode()
        if 'no comments found for current user' in error_text:
            return PostComment.NO_EXISTING_COMMENTS

        elif COMMENTING_NOT_ALLOWED in error_text:
            rich.print(f'Cannot post a comment: {error_text}')
            return PostComment.NOT_ALLOWED

        raise


def ci():   # noqa: C901, WPS210, WPS213, WPS231
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

    test_with_artifacts()

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
        comment_body_parts.append('## 🎉 Newly passed!')

        for test_name in newly_passed:
            comment_body_parts.append(f'* 🟢 `{test_name}`')

    if newly_failed:
        comment_body_parts.append('## 💥 Newly failed')

        for test_name in newly_failed:
            comment_body_parts.append(f'* 🔴 `{test_name}`')

    if not comment_body_parts:
        comment_body_parts.append('Nothing had changed in tests.')

    comment = COMMENT_TEMPLATE.format(
        body='\n\n'.join(comment_body_parts),
    )

    post_comment = gh.pr.comment.bake(_in=comment)

    if pr_number := os.environ.get('PR_NUMBER'):
        post_comment = post_comment.bake(pr_number)

    post_comment = post_comment.bake(body_file='-')

    recent_comment_edit = _post(post_comment.bake('--edit-last'))
    if recent_comment_edit == PostComment.NO_EXISTING_COMMENTS:
        _post(post_comment)

    if newly_failed:
        raise typer.Exit(1)


def serve():
    """
    Serve the iolanta.tech site.

    The site will be available at http://localhost:9841
    """
    sh.mkdocs.serve(
        '-a', 'localhost:6453',
        _fg=True,
    )


def install_mkdocs_insiders():
    """Install Insiders version of `mkdocs-material` theme."""
    name = 'mkdocs-material-insiders'

    if not (Path.cwd() / name).is_dir():
        sh.gh.repo.clone(f'iolanta-tech/{name}')

    sh.pip.install('-e', name)


def deploy_to_github_pages():
    """Build the docs & deploy → gh-pages branch."""
    sh.mkdocs('gh-deploy', '--force', '--clean', '--verbose')


def demonstrate_need_to_reset_cache():
    """Fail if cache is not reset in expand()."""
    yaml_ld.expand(
        'file:///home/anatoly/projects/iolanta/iolanta/data/'
        'textual-browser.yaml',
    )

    expanded = jsonld.expand(
        {
            '@context': {
                '@import': (
                    'https://json-ld.org/contexts/dollar-convenience.jsonld'
                ),
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                'iolanta': 'https://iolanta.tech/',
                '@base': 'https://iolanta.tech/visualizations/',
                'x': {'@id': 'iolanta:visualized-with', '@type': '@id'},
            },
            '$id': 'https://iolanta.tech/visualizations/index.yaml',
            'rdfs:label': 'Iolanta visualizations index 1.0',
            '$included': [
                {'$id': 'rdfs:', 'x': 'rdfs.yaml'},
                {
                    '$id': 'http://xmlns.com/foaf/0.1/',
                    'x': 'foaf.yaml',
                },
            ],
        },
    )

    raise ValueError(expanded[0]['@included'])
