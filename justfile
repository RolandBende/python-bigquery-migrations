# List available migrations
list-migrations:
    python3 -m src.bigquery_migrations.migration_cli list

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