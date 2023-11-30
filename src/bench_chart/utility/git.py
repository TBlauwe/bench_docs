import subprocess
import os
from asserts import assert_directory_exists


class Repository:
    def __init__(self, local_directory: str, hash_or_tag: str):
        assert_directory_exists(local_directory)
        self.local_directory = local_directory

        self.commit = "HEAD"
        self.change_commit(hash_or_tag)

    def change_commit(self, hash_or_tag: str):
        assert self._is_valid_hash_or_tag(hash_or_tag), (f"Hash or tag \"{hash_or_tag}\" is not valid "
                                                         f"for git repository \"{self.local_directory}\"")
        self.commit = hash_or_tag

    def get_author(self):
        return self._execute_command(["show", "-s", "--format='%an'"])

    def get_datetime(self):
        return self._execute_command(["show", "-s", "--date=iso", "--format='%ci'"])

    def get_branch(self):
        return self._execute_command(['rev-parse', '--abbrev-ref'])

    def get_commit_message(self):
        return self._execute_command(["show", "-s", "--format='%B'"])

    def _is_valid_hash_or_tag(self, hash_or_tag):
        all_refs = self._execute_command(["show-ref", "--tags", "--heads"]).split('\n')
        return any(
            ref.split(' ')[1] == hash_or_tag or ref.split(' ')[1].split('/')[-1] == hash_or_tag for ref in all_refs)

    def _execute_command(self, command):
        result = subprocess.run(['git'] + command + [self.commit], capture_output=True, text=True,
                                cwd=self.local_directory)
        if result.returncode != 0:
            raise Exception(f"Failed to run command {' '.join(command)}: {result.stderr}")
        return result.stdout.strip()
