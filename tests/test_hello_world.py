import unittest
from src.hello_world import hello_world

class TestHelloWorld(unittest.TestCase):
    def test_hello_world_output(self):
        with self.assertLogs(level='INFO') as log:
            hello_world()
        self.assertIn('Hello, World!', log.output[0])

if __name__ == '__main__':
    unittest.main()