import unittest
from writer_agent import WriterAgent

class TestWriterAgent(unittest.TestCase):
    def setUp(self):
        self.agent = WriterAgent()

    def test_write_content(self):
        # Test writing valid content
        self.agent.write_content('Hello, World!')  # This should not raise an error

    def test_write_empty_content(self):
        # Test writing empty content
        with self.assertRaises(ValueError):
            self.agent.write_content('')  # Assuming it raises an error

if __name__ == '__main__':
    unittest.main()