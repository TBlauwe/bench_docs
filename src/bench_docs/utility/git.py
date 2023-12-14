import subprocess
from bench_docs.utility.asserts import assert_directory_exists


class Repository:
    def __init__(self, local_directory: str):
        assert_directory_exists(local_directory)
        self.local_directory = local_directory

        self.commit = "HEAD"
        self.commit = self._get_latest_commit()

    def change_commit(self, hash_or_tag: str):
        self.commit = hash_or_tag
        assert self._is_valid_hash_or_tag(), (f"Hash or tag \"{hash_or_tag}\" is not valid "
                                              f"for git repository \"{self.local_directory}\"")

    def get_author(self):
        return self._execute_command(["show", "-s", "--format='%an'"])

    def get_datetime(self):
        return self._execute_command(["show", "-s", "--date=iso", "--format='%cd'"])

    def get_branch(self):
        if self.commit == "HEAD":
            return self._execute_command(['rev-parse', '--abbrev-ref'])
        else:
            branches = self._execute_command(['branch', '--contains']).split('\n')
            return branches[0].lstrip('* ')

    def get_commit_message(self):
        return self._execute_command(["show", "-s", "--format='%B'"])

    def _get_latest_commit(self):
        return self._execute_command(["rev-parse"])

    def _is_valid_hash_or_tag(self):
        return not self._execute_command(["cat-file", "-e"])

    def _execute_command(self, command):
        result = subprocess.run(['git'] + command + [self.commit],
                                capture_output=True, text=True, cwd=self.local_directory)
        if result.returncode != 0:
            raise Exception(f"Failed to run command {' '.join(command)}: {result.stderr}")
        return result.stdout.strip()
