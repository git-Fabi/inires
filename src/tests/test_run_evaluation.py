import logging
from src.utils.evaluation import run_evaluation_loop

# Test inputs that previously caused the error
current_plan_str = 'invalid_plan_structure'
ticket_context = {'some_key': 'some_value'}

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        run_evaluation_loop(current_plan_str, ticket_context)
    except Exception as e:
        logging.error(f'Test failed with error: {e}')
