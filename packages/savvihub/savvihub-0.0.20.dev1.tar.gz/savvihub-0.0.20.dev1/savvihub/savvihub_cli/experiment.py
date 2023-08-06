import re
from datetime import datetime
from typing import List

import typer
from terminaltables import AsciiTable
import inquirer

from savvihub.common.context import Context
from savvihub.common.git import GitRepository, InvalidGitRepository
from savvihub.savvihub_cli.inquirer import get_choices, parse_title
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import CUR_DIR, INQUIRER_NAME_IMAGE, INQUIRER_NAME_RESOURCE, \
    INQUIRER_NAME_COMMAND, WEB_HOST, INQUIRER_NAME_DATASET, INQUIRER_NAME_DATASET_REF, \
    INQUIRER_NAME_DATASET_MOUNT_PATH, DEFAULT_SAVVIHUBFILE_YAML
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.common.utils import *

experiment_app = typer.Typer()


@experiment_app.callback()
def main():
    """
    Perform your experiment with Savvihub
    """
    return


@experiment_app.command()
def list():
    """
    List of experiments
    """
    try:
        git_repo = GitRepository()
    except InvalidGitRepository as e:
        typer.echo(str(e))
        return

    context = Context(project_required=True, project_config_path=git_repo.get_savvihub_config_file_path())
    client = SavviHubClient(token=context.token)

    experiments = client.experiment_list(context.workspace, context.project, raise_error=True)
    table = AsciiTable([
        ['Number', 'Status', 'Message'],
        *[[e.number, e.status, e.message] for e in experiments],
    ])
    typer.echo(table.table)


@experiment_app.command()
def logs(
    experiment_number: int = typer.Argument(...),
):
    """
    View experiment logs
    """
    try:
        git_repo = GitRepository()
    except InvalidGitRepository as e:
        typer.echo(str(e))
        return

    context = Context(project_required=True, project_config_path=git_repo.get_savvihub_config_file_path())
    client = SavviHubClient(token=context.token)

    logs = client.experiment_log(context.workspace, context.project, experiment_number, raise_error=True)
    for log in logs:
        print(datetime.fromtimestamp(log.timestamp), log.message)


@experiment_app.command()
def run(
    command_arg: str = typer.Option(None, "-c"),
    image_arg: str = typer.Option(None, "-i"),
    resource_arg: str = typer.Option(None, "-r"),
    env_vars_arg: List[str] = typer.Option([], "-e"),
    dataset_mount_args: List[str] = typer.Option([], "--dataset"),
):
    """
    Run an experiment in Savvihub
    """
    try:
        git_repo = GitRepository()
    except InvalidGitRepository as e:
        typer.echo(str(e))
        return

    context = Context(project_required=True, project_config_path=git_repo.get_savvihub_config_file_path())
    client = SavviHubClient(token=context.token)

    def find_from_args(options, selector):
        for option in options:
            if selector(option):
                return option
        return None

    selected_image, selected_resource, start_command = None, None, None

    images = client.kernel_image_list(context.workspace)
    if image_arg:
        selected_image = find_from_args(images, lambda x: x.image_url == image_arg.strip())
        if selected_image is None:
            typer.echo(f'Cannot find image {image_arg}.')
            return
    else:
        answers = inquirer.prompt([inquirer.List(
            INQUIRER_NAME_IMAGE,
            message="Please choose a kernel image",
            choices=[f'[{i+1}] {image.image_url} ({image.name})' for i, image in enumerate(images)],
        )])
        answer = int(re.findall(r"[\d+]", answers.get(INQUIRER_NAME_IMAGE))[0]) - 1
        selected_image = images[answer]

    resources = client.kernel_resource_list(context.workspace)
    if resource_arg:
        selected_resource = find_from_args(resources, lambda x: x.name == resource_arg.strip())
        if selected_resource is None:
            typer.echo(f'Cannot find resource {resource_arg}.')
            return
    else:
        answers = inquirer.prompt([inquirer.List(
            INQUIRER_NAME_RESOURCE,
            message="Please choose a kernel resource",
            choices=[f'[{i+1}] {resource.name}' for i, resource in enumerate(resources)]
        )])
        answer = int(re.findall(f"[\d+]", answers.get(INQUIRER_NAME_RESOURCE))[0]) - 1
        selected_resource = resources[answer]

    if command_arg:
        start_command = command_arg
    else:
        answers = inquirer.prompt([inquirer.Text(
            INQUIRER_NAME_COMMAND,
            message="Start command",
            default="python main.py",
        )])
        answer = answers.get(INQUIRER_NAME_COMMAND)
        start_command = answer

    dataset_mounts_parsed = []
    for dataset_mount in dataset_mount_args:
        # parse dataset and volume
        if ':' not in dataset_mount:
            typer.echo(f'Invalid dataset slug: {dataset_mount}. '
                       f'You should specify dataset mount location.\n'
                       f'ex) savvihub/mnist@3d1e0f:/input/dataset1')
            return
        dataset, mount_path = dataset_mount.split(':')

        # parse snapshot ref
        if '@' in dataset:
            dataset_slug, snapshot_ref = dataset.split('@')
        else:
            dataset_slug = dataset
            snapshot_ref = 'latest'

        if '/' not in dataset_slug:
            typer.echo(f'Invalid dataset slug: {dataset_mount}. '
                       f'You should specify dataset with workspace.\n'
                       f'ex) savvihub/mnist@3d1e0f:/input/dataset1')
            return
        workspace, dataset = dataset_slug.split('/')

        # read dataset or snapshot
        dataset_obj = client.dataset_read(workspace, dataset)
        if not dataset_obj:
            typer.echo(f'Invalid dataset: {dataset_mount}. '
                       f'Please check your dataset exist in savvihub.\n')
            return
        if snapshot_ref != 'latest':
            snapshot_obj = client.snapshot_read(dataset_obj.main_volume_id, snapshot_ref)
            if not snapshot_obj:
                typer.echo(f'Invalid dataset snapshots: {dataset_mount}. '
                           f'Please check your dataset and snapshot exist in savvihub.')
                return

        dataset_mounts_parsed.append(dict(
            dataset_id=dataset_obj.id,
            snapshot_ref=snapshot_ref,
            mount_path=mount_path,
        ))

    revision_or_branch, is_revision = git_repo.get_remote_revision_or_branch()
    revision, branch = None, None
    if is_revision:
        revision = revision_or_branch
    else:
        branch = revision_or_branch

    diff_file = git_repo.get_current_diff_file(revision_or_branch)

    res = client.experiment_create(
        workspace=context.workspace,
        project=context.project,
        image_id=selected_image.id,
        resource_spec_id=selected_resource.id,
        git_ref=revision_or_branch,
        start_command=start_command,
        dataset_mount_infos=dataset_mounts_parsed,
    )

    diff_file.close()

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        return
    res.raise_for_status()

    experiment_number = res_data.get('number')
    typer.echo(f"Experiment {experiment_number} is running. Check the experiment status at below link")
    typer.echo(f"{WEB_HOST}/{context.workspace}/{context.project}/"
               f"experiments/{experiment_number}")
    return


if __name__ == "__main__":
    experiment_app()
