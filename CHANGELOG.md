# Changelog

## 0.5.4

### Security

- Upgraded `cryptography` from `46.0.5` to `50.0.0` to fix three CVEs:
    - PKCS#7 `EnvelopedData` decryption exposes a Bleichenbacher oracle through distinguishable errors and timing (`CVE-2026-69247`, fixed in `50.0.0`)
    - Buffer overflow when non-contiguous buffers are passed to APIs accepting Python buffer protocol objects (`CVE-2026-39892`, fixed in `46.0.7`)
    - Name constraints not applied to peer names when the leaf certificate contains a wildcard DNS SAN (`CVE-2026-34073`, fixed in `46.0.6`)
- Added explicit `cryptography>=50.0.0` lower-bound in `pyproject.toml` to protect downstream consumers

### Fix

- Fixed PEP 8 style violations in `migration_cli.py` (E302: missing blank lines before top-level functions) and `migration_manager.py` (W293: whitespace on blank line, E303: too many blank lines inside class)

## 0.5.3

### Security

- Upgraded `protobuf` from `5.29.1` to `6.33.6` to fix two high-severity CVEs:
    - JSON recursion depth bypass (`protobuf < 5.29.6`)
    - Denial of Service via recursive groups in pure-Python backend (`protobuf < 5.29.5`)
- Upgraded `google-cloud-bigquery` from `3.27.0` to `3.40.1`
- Upgraded `google-auth` from `2.37.0` to `2.49.1`
- Upgraded `google-api-core` from `2.24.0` to `2.30.0`
- Upgraded `grpcio` / `grpcio-status` from `1.68.1` to `1.78.0`
- Added explicit `protobuf>=5.29.6` lower-bound in `pyproject.toml` to protect downstream consumers

### Fix

- `migration_cli.py`: `--gcp-sa-json-dir` and `--gcp-sa-json-fname` CLI arguments were silently ignored due to both reading from `args.migrations_dir` instead of their own argument attributes

### Removed

- Dropped Python 3.9 support (EOL since October 2025). The updated security dependency chain (`cryptography>=46`, `cffi>=2.0`, `pycparser==3.0`) requires Python >=3.10. Minimum supported version is now Python 3.10

## 0.5.2.

### Feature

- Rollback the last migration

### Documentation

- README.md
    - Modified sections
        - Getting Started
        - Rolling Back Migrations


## 0.5.1

### Documentation

- README.md
    - Modified sections
        - Create the neccessary files in the folders

## 0.5.0

### Feature

- Rollback to a specific migration

### Documentation

- README.md
    - New sections
        - Migration log
    - Modified sections
        - Running migrations
        - Rollback migrations

## 0.4.3

### Documentation

- README.md
    - GCP Service account creation process updated

## 0.4.2

### Documentation

- README.md
    - Sample code: import correction
    - New sections:
        - GCP Service account creation process
        - Migration naming convention

## 0.4.1

### Documentation

- README.md sample code: removed unnecessary lines of code

## 0.4.0

This is the first release which uses the `CHANGELOG` file.