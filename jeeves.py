import os

from sh import git, pytest, tee


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    git.submodule.update('--remote', '--init', '--recursive')


def ci():
    """Run CI."""
    env = {
        **os.environ,
        'PYTEST_RUN_PATH': 'tests',
    }

    tee(
        'tests/coverage/pytest-coverage.txt',
        _in=pytest(
            'tests',
            junitxml='tests/coverage/pytest.xml',
            cov='yaml_ld',
            _piped=True,
            _ok_code={0, 1},
            _env=env,
        ),
        _env=env,
    )
