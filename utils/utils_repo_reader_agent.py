import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def prepare_repo_reader_input(repository_files):
    if len(repository_files) == 0:
        logging.warning('Repository files list is empty')
        return None
    # Processing repository_files here


def _scan_repository_filesystem():
    # Simulated function to scan the filesystem
    repository_files = []  # Replace with actual scanning logic
    logging.info(f'Total files found: {len(repository_files)}')
    if len(repository_files) == 0:
        logging.error('No files found in the repository')
    return repository_files
