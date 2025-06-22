import subprocess

def test_hello():
    result = subprocess.run(['python3', '/home/runner/work/inires/inires/src/hello.py'], capture_output=True, text=True)
    assert result.stdout.strip() == 'Hello World'
