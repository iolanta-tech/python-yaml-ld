from sh import git, pytest, tee


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    git.submodule.update('--remote', '--init', '--recursive')


def ci():
    """Run CI."""
    tee(
        'tests/coverage/pytest-coverage.txt',
        _in=pytest(
            'tests',
            junitxml='tests/coverage/pytest.xml',
            cov_report=['', 'html:tests/coverage/html'],
            cov='yaml_ld',
            _piped=True,
            _ok_code={0, 1},
        ),
    )
