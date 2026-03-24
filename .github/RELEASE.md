# Release Process

This document describes the full release workflow for `bigquery-migrations` — from local development and testing through to publishing on PyPI.

---

## Prerequisites

- **pyenv** installed (`brew install pyenv`)
- **Python 3.12** installed via pyenv (`pyenv install 3.12.13`)
- **GitHub CLI** installed (`brew install gh`)
- **TestPyPI** and **PyPI** accounts with trusted publishing configured (OIDC via GitHub Actions environment)
- GCP service account JSON at `credentials/gcp-sa.json`
- `GCP_PROJECT_ID` known

---

## Step 1 — Local Development Setup

Set up a clean Python 3.12 environment for development and testing:

```bash
# Pin Python version for this project
pyenv local 3.12.13

# Create fresh virtual environment
rm -rf env
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 2 — Make Changes

Edit source files under `src/bigquery_migrations/`.

When dependencies change (new packages or version upgrades), upgrade and re-freeze:

```bash
pip install --upgrade <package-name>
just save-packages   # pip freeze > requirements.txt
```

---

## Step 3 — Update Version and Changelog

**Semantic versioning rules:**
- `PATCH` (e.g. `0.5.2` → `0.5.3`): bug fixes, security patches, no API changes
- `MINOR` (e.g. `0.5.x` → `0.6.0`): new backwards-compatible features
- `MAJOR` (e.g. `0.x.x` → `1.0.0`): breaking changes

**1. Bump the version** in `src/bigquery_migrations/__init__.py`:
```python
__version__ = "0.5.3"
```

**2. Add a CHANGELOG entry** in `CHANGELOG.md` following this structure:
```markdown
## 0.5.3

### Security
- ...

### Feature
- ...

### Fix
- ...

### Documentation
- ...

### Removed
- ...
```

Only include sections that are relevant for the release.

---

## Step 4 — Run Unit Tests Locally (Baseline)

Verify all tests pass before committing anything:

```bash
just test-unit-all
```

Expected output: all tests green, `OK`.

Also run linters:

```bash
just test-flake8
just test-ruff
```

---

## Step 5 — Run Integration Tests Locally

Test against a real BigQuery database using the local source code.

```bash
source env/bin/activate
export GCP_PROJECT_ID="your-gcp-project-id"

# List available migrations
just migrations-list

# Run all pending migrations (calls up())
just migrations-run

# Verify in BigQuery console that expected datasets/tables were created

# Rollback the last migration (calls down())
just migrations-rollback-last

# Or rollback everything
just migrations-reset
```

> **Note:** `just migrations-run` uses `python3 -m src.bigquery_migrations.migration_cli` which runs directly from the local `src/` folder — no build or install needed.

---

## Step 6 — Commit and Push

Stage only the relevant changed files:

```bash
git add CHANGELOG.md \
        pyproject.toml \
        requirements.txt \
        src/bigquery_migrations/__init__.py \
        src/bigquery_migrations/migration_cli.py  # (if changed)
```

Use [Conventional Commits](https://www.conventionalcommits.org/) for the commit message. For a patch/security release:

```bash
git commit -m "fix(deps): upgrade protobuf to 6.33.6 to patch high-severity CVEs

Fixes JSON recursion depth bypass and DoS vulnerability in pure-Python
protobuf backend. Also upgrades google-cloud-bigquery, google-auth,
google-api-core, grpcio, and adds protobuf>=5.29.6 lower-bound."
```

Then push:

```bash
git push origin main
```

---

## Step 7 — Wait for CI to Pass

The `Run Tests` GitHub Actions workflow triggers automatically on every push. It runs unit tests across Python 3.10–3.13 and all linters.

Monitor at:
```
https://github.com/RolandBende/python-bigquery-migrations/actions
```

**Do not proceed until all checks are green.**

---

## Step 8 — Publish to TestPyPI

Trigger the TestPyPI publish workflow manually in GitHub Actions:

1. Go to: `https://github.com/RolandBende/python-bigquery-migrations/actions/workflows/testpypi-publish.yaml`
2. Click **"Run workflow"** → select `main` branch → click **"Run workflow"**

Once complete, the new version appears at:
```
https://test.pypi.org/p/bigquery-migrations
```

---

## Step 9 — Test the Published Package from TestPyPI

Create a clean environment and install from TestPyPI:

```bash
mkdir /tmp/bq-migrations-test && cd /tmp/bq-migrations-test
~/.pyenv/versions/3.12.13/bin/python3 -m venv env && source env/bin/activate

pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  bigquery-migrations==0.5.3
```

> **Important:** Always use both `--index-url` (TestPyPI) and `--extra-index-url` (real PyPI).
> Using only `-i https://test.pypi.org/simple/` will fail because dependencies like
> `google-cloud-bigquery` are not on TestPyPI.

Verify the installation:

```bash
python3 -c "import bigquery_migrations; print(bigquery_migrations.__version__)"
# Expected: 0.5.3

bigquery-migrations --help
```

Run integration tests using the installed CLI:

```bash
export GCP_PROJECT_ID="your-gcp-project-id"

bigquery-migrations list \
  --gcp-sa-json-dir /path/to/credentials \
  --gcp-sa-json-fname gcp-sa.json \
  --migrations-dir /path/to/migrations

bigquery-migrations run \
  --gcp-sa-json-dir /path/to/credentials \
  --gcp-sa-json-fname gcp-sa.json \
  --migrations-dir /path/to/migrations

# Verify in BigQuery console, then rollback
bigquery-migrations reset \
  --gcp-sa-json-dir /path/to/credentials \
  --gcp-sa-json-fname gcp-sa.json \
  --migrations-dir /path/to/migrations
```

> **Note:** Migration files must use `from bigquery_migrations.migration import Migration`
> (not `from src.bigquery_migrations...`) when running via the installed CLI.

---

## Step 10 — Create a GitHub Release (triggers production PyPI publish)

Once TestPyPI testing is confirmed working, create a GitHub Release using the GitHub CLI:

```bash
gh release create v0.5.3 \
  --title "v0.5.3" \
  --notes "### Security
- Upgraded \`protobuf\` from \`5.29.1\` to \`6.33.6\` (CVE: JSON recursion bypass, DoS)
- Upgraded \`google-cloud-bigquery\`, \`google-auth\`, \`google-api-core\`, \`grpcio\`
- Added \`protobuf>=5.29.6\` lower-bound in \`pyproject.toml\`

### Fix
- \`--gcp-sa-json-dir\` and \`--gcp-sa-json-fname\` CLI args were silently ignored

### Removed
- Dropped Python 3.9 support (EOL since October 2025)"
```

This automatically:
- Creates the `v0.5.3` tag on `main`
- Creates the GitHub Release entry
- Triggers the `pypi-publish.yaml` workflow which builds and publishes to production PyPI

Monitor the publish workflow at:
```
https://github.com/RolandBende/python-bigquery-migrations/actions/workflows/pypi-publish.yaml
```

Once green, the new version is live at:
```
https://pypi.org/p/bigquery-migrations
```

---

## Quick Reference Checklist

```
[ ] Bump __version__ in src/bigquery_migrations/__init__.py
[ ] Add CHANGELOG.md entry
[ ] just test-unit-all  →  all green
[ ] just test-flake8 && just test-ruff  →  clean
[ ] Integration test locally (just migrations-run / reset)
[ ] git add / commit / push origin main
[ ] Wait for CI (Run Tests) to pass on GitHub Actions
[ ] Trigger TestPyPI workflow manually in GitHub Actions
[ ] Install from TestPyPI in clean venv and verify
[ ] Integration test via installed CLI
[ ] gh release create vX.Y.Z ...  →  triggers production PyPI publish
[ ] Verify on https://pypi.org/p/bigquery-migrations
```
