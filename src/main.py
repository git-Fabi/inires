from src.agents.writer_agent import WriterAgent

# Assuming commit_hashes is a list of commit hashes to revert
commit_hashes = ['hash1', 'hash2']  # Replace with actual commit hashes
agent = WriterAgent(name='MainAgent')

for commit_hash in commit_hashes:
    revert_result = agent.git_revert(commit_hash)
    print(revert_result)  # You may want to log this or handle it differently.