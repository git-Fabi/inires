# Contribution guidelines

This project enforces code quality and security using:

- [`black`](https://black.readthedocs.io/en/stable/): Code formatter
- [`ruff`](https://docs.astral.sh/ruff/): Linter and style checker
- [`mypy`](https://mypy-lang.org/): Static type checker
- [`bandit`](https://bandit.readthedocs.io/en/latest/): Security analyzer
- [`radon`](https://radon.readthedocs.io/en/latest/): Code complexity analysis

---

## Installation

Create and activate your virtual environment, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install black ruff bandit radon
````

---

## Code Quality Checks

Run the following tools before committing code:

### Format Code

```bash
black .
```

### Lint Code

```bash
ruff .
```

### Static Type checking

```bash
mypy .
```

### Check Security

```bash
bandit -r .
```

### Analyze Complexity

```bash
radon cc . -s -a
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
git checkout -b feature/<short-feature-name>
```

---

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
