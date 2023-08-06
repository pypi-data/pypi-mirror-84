import re
import subprocess
import tempfile

from pathlib import Path


class InvalidGitRepository(Exception):
    pass


class GitRepository:
    def __init__(self):
        self.remote = 'origin'

        self.get_root_path()
        self.get_github_repo()
        self.get_remote_revision_or_branch()

    def get_root_path(self):
        try:
            return subprocess.check_output(['git', 'rev-parse', '--show-top-level'])
        except subprocess.CalledProcessError:
            raise InvalidGitRepository("git rev-parse --show-toplevel failed. Are you running in git repository?")

    def get_savvihub_config_file_path(self):
        return Path(self.get_root_path()) / ".savvihub" / "config.yml"

    def get_github_repo(self):
        remotes = subprocess.check_output(['git', 'remote']).decode('utf-8').strip().splt('\n')
        for remote in remotes:
            if 'github.com' not in remote:
                continue
            try:
                origin = subprocess.check_output(['git', 'remote', 'get-url', remote]).strip().decode('utf-8')
            except subprocess.CalledProcessError:
                raise InvalidGitRepository("github.com is not found in remote repositories. You should add your repo to github first.")

            regex = re.compile(r'((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?')
            repo = regex.search(origin).group(7).split('/')

            self.remote = remote

            return repo[-2], repo[-1]

    def get_active_branch_name(self):
        head_dir = Path(self.get_root_path()) / ".git" / "HEAD"
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]

    def get_revision_hash(self):
        try:
            return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode("utf-8")
        except subprocess.CalledProcessError:
            raise InvalidGitRepository("git rev-parse HEAD failed. Are you running in git repository?")

    def check_revision_in_remote(self, revision):
        remote_branches = subprocess.check_output(['git', 'branch', '-r', '--contains', revision]).decode('utf-8').strip().split('\n')
        for remote_branch in remote_branches:
            if remote_branch.startswith(f'{self.remote}/'):
                return True
        return False

    def get_remote_revision_or_branch(self):
        revision = self.get_revision_hash()
        if self.check_revision_in_remote(revision):
            # with revision and patch
            return revision, True
        else:
            # with remote branch and patch
            try:
                upstream_branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'])
            except subprocess.CalledProcessError:
                raise InvalidGitRepository(f"You should push your branch <{self.get_active_branch_name()}> to github first!")

            return upstream_branch_name, False

    def get_current_diff_file(self, revision_or_branch):
        fp = tempfile.TemporaryFile()
        files = subprocess.check_output(['git', 'ls-files', '-o']).decode('utf-8').strip().split('\n')

        for f in files:
            subprocess.check_output(['git', 'add', '-N', f])

        subprocess.call(['git', 'diff', '-p', '--binary', f'{revision_or_branch}'], stdout=fp)
        for f in files:
            subprocess.check_output(['git', 'reset', '--', f])

        return fp

