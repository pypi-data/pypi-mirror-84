import os

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import WEB_HOST
from savvihub.common.git import GitRepository, InvalidGitRepository
from savvihub.common.utils import make_file, remove_file
from savvihub.savvihub_cli.yml_loader import ProjectYmlLoader

project_app = typer.Typer()


@project_app.callback()
def main():
    return


@project_app.command()
def init(
    slug: str = typer.Argument(..., help="Type workspace/project as an argument"),
):
    """
    Initialize a new experiment configuration file with workspace/project
    """
    try:
        git_repo = GitRepository()
    except InvalidGitRepository as e:
        typer.echo(str(e))
        return

    config_file_path = git_repo.get_savvihub_config_file_path()
    if os.path.exists(config_file_path):
        answer = typer.prompt(f'Savvihub config file already exists in {config_file_path} Overwrite file? [Y/n] ')
        if answer.lower().startswith('y'):
            remove_file(config_file_path)
        else:
            return

    workspace_slug, project_slug = slug.split("/")
    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    workspace = client.workspace_read(workspace_slug)
    if workspace is None:
        typer.echo(f'Cannot find workspace {workspace}.')
        return

    project = client.project_read(workspace_slug, project_slug)
    if project is None:
        owner, repo = git_repo.get_github_repo()
        create_new_project = typer.prompt(f'Project not found. Create new project in SavviHub? [Y/n] ')
        if create_new_project.lower().strip().startswith('y'):
            if not context.me.github_authorized:
                typer.echo(f'You should authorize github first.\nhttp://{WEB_HOST}/github/authorize/')
                return

            typer.echo(f'Workspace: {workspace_slug}\nProject: {project_slug}\nGit: github.com/{owner}/{repo}')
            client.project_github_create(workspace_slug, project_slug, owner, repo, raise_error=True)
            typer.echo(f'Project created successfully.\nhttp://{WEB_HOST}/{workspace_slug}/{project_slug}')

    data = {
        'workspace': workspace_slug,
        'project': project_slug,
    }

    make_file(config_file_path)
    yml_loader = ProjectYmlLoader(config_file_path)
    yml_loader.write(data)

    typer.echo(f"Experiment config successfully made in {config_file_path}")
