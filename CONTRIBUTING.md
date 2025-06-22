# Contribution guidelines

This project enforces code quality and security using:

- [`black`](https://black.readthedocs.io/en/stable/): Code formatter
- [`ruff`](https://docs.astral.sh/ruff/): Linter and style checker
- [`mypy`](https://mypy-lang.org/): Static type checker
- [`bandit`](https://bandit.readthedocs.io/en/latest/): Security analyzer
- [`radon`](https://radon.readthedocs.io/en/latest/): Code complexity analysis
- [`pytest`](https://docs.pytest.org/en/stable/): Testing framework

---

## Installation

First, install [`uv`](https://github.com/astral-sh/uv), a fast Python package manager and virtual environment tool.

You can install it using **`curl`**:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```
Or using pip (requires Python ≥3.8):
```bash
pip install uv
```
- If installed via curl, uv will be located at ~/.cargo/bin/uv. Make sure that directory is in your $PATH.
- If installed via pip, the uv command will be available in your Python environment’s bin directory.

### Set up your environment and install dependencies

```bash
# Create and activate a virtual environment using uv
uv .venv .venv
source .venv/bin/activate
```

Option 1: Using pyproject.toml (recommended)

```bash
# Install all dependencies defined in pyproject.toml
uv pip install -e .[dev]
```

Option 2: Using requirements-dev.txt

```bash
# Install dependencies from requirements-dev.txt using uv
uv pip install -r requirements-dev.txt
```

---

## Git Branching Strategy

| Prefix      | Purpose                                       | Example Branch Name           |
| ----------- | --------------------------------------------- | ----------------------------- |
| `feat/`     | New feature or enhancement                    | `feat/1234-user-login`        |
| `fix/`      | Bug fix                                       | `fix/5678-null-pointer-crash` |
| `bugfix/`   | Alternative to `fix/`, more explicit          | `bugfix/7890-ui-freeze`       |
| `hotfix/`   | Critical fix, often for production            | `hotfix/urgent-prod-issue`    |
| `chore/`    | Routine tasks, cleanup, no logic change       | `chore/cleanup-unused-files`  |
| `refactor/` | Code restructuring without behavior change    | `refactor/auth-service`       |
| `docs/`     | Documentation updates                         | `docs/api-endpoint-specs`     |
| `test/`     | Adding or updating tests                      | `test/improve-coverage-login` |
| `ci/`       | CI/CD configuration or pipeline changes       | `ci/cache-optimization`       |
| `build/`    | Build system or tooling changes               | `build/update-webpack-config` |
| `infra/`    | Infrastructure as code (e.g., IaC, pipelines) | `infra/terraform-setup`       |
| `revert/`   | Reverting a previous commit or branch         | `revert/feat-login-refactor`  |
| `devops/`   | DevOps tooling, deployment setup              | `devops/enable-auto-scaling`  |  



### Creating a Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feat/<issue-number>-<short-description>
```

## Code Quality Checks

Run the following tools before committing code:

### Format Code

```bash
black src/ tests/
```

### Lint Code

```bash
ruff check src/ tests/
```

### Static Type checking

```bash
mypy --strict --ignore-missing-imports --explicit-package-bases src/ tests/
```

### Check Security

```bash
bandit -r src/ tests/ --skip B101
```

### Analyze Complexity

```bash
radon cc src/ tests/
radon mi src/ tests/
```

---

## Testing

We use pytest for unit and integration testing.
Running Tests

From the project root:

pytest tests/

To run with coverage:

pytest --cov=inires tests/

Writing Tests

    Add tests in the tests/ directory.

    Name your test files like test_<module>.py.

    Use descriptive test function names (e.g. test_agent_returns_multiple_suggestions()).

    Use fixtures and mocking where appropriate.

Test Guidelines

    Write tests for new features and bug fixes.

    Aim for at least 80% coverage.

    Include both happy path and edge cases.

    If your feature is difficult to test, explain why in the PR.

## Using Pre-commit Hooks

We use [pre-commit](https://pre-commit.com/) hooks to keep the codebase clean, consistent, and secure. Before every commit, the configured hooks will automatically check your code for formatting, linting, typing, security issues, and complexity.

### How to install pre-commit hooks

Run this command once after cloning the repo:

```bash
pre-commit install
```


## Pull Request Workflow

1. **Create a PR** against the `main` branch.
2. Ensure:

   * Code passes **Black**, **Ruff**, **MyPy**, **Bandit**, and **Radon** checks.
   * Commits are clear and atomic.
   * PR description includes:

     * Purpose
     * Relevant issue/ticket
     * Test details
3. Wait for at least **one approval** before merging.

### Example PR Template

```
### Summary
Briefly describe what this PR does.

### Related Issues
Fixes #123

### Changes
- Added feature X
- Refactored Y

### Checklist
- [ ] Code formatted with `black`
- [ ] Linted with `ruff`
- [ ] Typed and checked with `mypy`
- [ ] Security checked with `bandit`
- [ ] Complexity reviewed with `radon`
- [ ] Added/updated tests
- [ ] Ready for review
```

---
