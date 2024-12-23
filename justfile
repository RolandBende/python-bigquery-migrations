# Creating a Virtual env.
create-env:
    python3 -m venv env

# Save required packages
save-packages:
    pip freeze > requirements.txt

# Install required packages
install-packages:
    pip install -r requirements.txt

# Build package
build:
    python3 -m build

# Validate build
build-check:
    twine check dist/*

# Delete build
build-delete:
    rm -rf __pycache__ dist build src/*.egg-info

# Upload to TestPyPi
upload-test:
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to PyPi
upload-prod:
    twine upload dist/*

# List available migrations
migrations-list:
    python3 -m src.bigquery_migrations.migration_cli list

# Run migrations
migrations-run:
    python3 -m src.bigquery_migrations.migration_cli run

# Rollback migration
migrations-rollback-last:
    python3 -m src.bigquery_migrations.migration_cli rollback --migration-name last

# Rollback migrations
migrations-rollback-specified:
    python3 -m src.bigquery_migrations.migration_cli rollback --migration-name 2024_12_10_121000_create_users_table

# Rollback all migrations
migrations-reset:
    python3 -m src.bigquery_migrations.migration_cli reset

# Unit testing: all
test-unit-all:
    python3 -m unittest discover tests -v

# Unit test: single file
test-unit-single *ARGS:
    python3 -m unittest tests/unit/test_{{ ARGS }}.py

# Unit test coverage
test-unit-coverage:
    coverage run -m unittest discover
    coverage report --skip-empty

# PEP8 tests: autopep8
test-autopep8:
    autopep8 src/bigquery_migrations/*

# PEP8 tests: flake8
test-flake8:
    flake8 src/bigquery_migrations/*

# PEP8 tests: ruff
test-ruff:
    ruff check src/bigquery_migrations/