from sh import git


def update_submodule():
    """Update the `specification` submodule from GitHub."""
    git.submodule.update('--remote')
