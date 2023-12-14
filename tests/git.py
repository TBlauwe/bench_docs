import unittest
from bench_docs.utility import git


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # This runs before each test
        self.repo = git.Repository("../")

    def test_get_author(self):
        self.assertTrue(self.repo.get_author())

    def test_get_datetime(self):
        self.assertTrue(self.repo.get_datetime())

    def test_get_branch(self):
        self.assertTrue(self.repo.get_branch())

    def test_get_message(self):
        self.assertTrue(self.repo.get_commit_message())

    def test_change_commit(self):
        self.assertIsNone(self.repo.change_commit("c6b6a0bfcc582967aecfbb20d4efa042c3aefb7d"))


if __name__ == '__main__':
    unittest.main()
