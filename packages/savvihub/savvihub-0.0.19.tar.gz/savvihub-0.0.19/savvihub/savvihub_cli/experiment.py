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
def log(
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
    file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
    command: str = typer.Option(None, "-c"),
    image: str = typer.Option(None, "-i"),
    resource: str = typer.Option(None, "-r"),
    env_vars: List[str] = typer.Option([], "-e"),
    dataset_mounts: List[str] = typer.Option([], "--dataset"),
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

    questions = []
    if not image:
        questions.append(inquirer.List(
            INQUIRER_NAME_IMAGE,
            message="Please choose a kernel image",
            choices=get_choices(client, 'image', context.workspace),
        ))

    if not resource:
        questions.append(inquirer.List(
            INQUIRER_NAME_RESOURCE,
            message="Please choose a kernel resource",
            choices=get_choices(client, 'resource', context.workspace),
        ))

    if not command:
        questions.append(
            inquirer.Text(
                INQUIRER_NAME_COMMAND,
                message="Start command",
                default="python main.py",
            )
        )

    answers = []
    if questions:
        answers = inquirer.prompt(questions)

    if not image:
        image = parse_title(answers.get(INQUIRER_NAME_IMAGE))

    if not resource:
        resource = parse_title(answers.get(INQUIRER_NAME_RESOURCE))

    if not command:
        command = answers.get(INQUIRER_NAME_COMMAND)

    dataset_mounts_parsed = []
    for dataset_mount in dataset_mounts:
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
            workspace=workspace,
            dataset=dataset,
            ref=snapshot_ref,
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
        image=image,
        resource_spec=resource,
        revision=revision,
        branch=branch,
        start_command=command,
        diff=diff_file,
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
