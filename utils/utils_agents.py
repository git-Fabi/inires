import logging

# Set up logging\logging.basicConfig(level=logging.INFO)

def runner(param1, param2):
    # Log input parameters
    logging.debug(f'Runner called with param1: {param1}, param2: {param2}') 
    
    # Example of accessing a tuple safely
    if isinstance(param1, tuple) and len(param1) > 0:
        value = param1[0]  # Access the first element safely
        logging.debug(f'Accessed tuple value: {value}')
    else:
        logging.warning('param1 is not a tuple or is empty')

    # Additional logic for runner function can be added here.