import unittest
from src.agents.writer_agent import WriterAgent
import subprocess


class TestWriterAgent(unittest.TestCase):
    def setUp(self):
        self.agent = WriterAgent(name='TestAgent')

    def test_git_revert(self):
        # Mock the subprocess.run method to simulate git revert
        with unittest.mock.patch('subprocess.run') as mocked_run:
            mocked_run.return_value.stdout = 'Revert successful'
            mocked_run.return_value.returncode = 0
            result = self.agent.git_revert('commit_hash')
            self.assertEqual(result, 'Revert successful')
            mocked_run.assert_called_once_with(['git', 'revert', 'commit_hash'], check=True, text=True, capture_output=True)

    def test_git_revert_failure(self):
        # Mock the subprocess.run method to simulate a failure in git revert
        with unittest.mock.patch('subprocess.run') as mocked_run:
            mocked_run.side_effect = subprocess.CalledProcessError(1, 'git revert')
            result = self.agent.git_revert('commit_hash')
            self.assertEqual(result, '')  # Expecting empty string on exception

    def test_check_set_upstream(self):
        # Mock the subprocess.run method to simulate successful push with --set-upstream
        with unittest.mock.patch('subprocess.run') as mocked_run:
            mocked_run.return_value.stdout = 'Push successful'
            mocked_run.return_value.returncode = 0
            result = self.agent.check_set_upstream()
            self.assertEqual(result, 'Push successful')
            mocked_run.assert_called_once_with(['git', 'push', '--set-upstream', 'origin', 'branch_name'], check=True, text=True, capture_output=True)

    def test_check_set_upstream_failure(self):
        # Mock the subprocess.run method to simulate a failure in push
        with unittest.mock.patch('subprocess.run') as mocked_run:
            mocked_run.side_effect = subprocess.CalledProcessError(1, 'git push')
            result = self.agent.check_set_upstream()
            self.assertEqual(result, '')  # Expecting empty string on exception


if __name__ == '__main__':
    unittest.main()