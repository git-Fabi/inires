import logging
from utils.utils_agents import runner

# Set up logging for testing\logging.basicConfig(level=logging.DEBUG)

def test_runner():
    # Test with normal input
    runner(('test_value',), 'param2')
    # Test with empty tuple
    runner((), 'param2')
    # Test with non-tuple
    runner('not_a_tuple', 'param2')

if __name__ == '__main__':
    test_runner()