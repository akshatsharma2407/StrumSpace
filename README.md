# StrumSpace

Backend foundation for the StrumSpace guitar academy management system.

## Development environment

- Python: 3.13.18
- Package and environment management: [uv](https://docs.astral.sh/uv/)

The supported Python range is defined in `pyproject.toml`, and `.python-version`
pins the project to the development version used locally.

### Set up the environment

Install uv, then run:

```bash
uv sync
```

This creates the project virtual environment in `.venv` and installs runtime and
development dependencies from `uv.lock`.

Run Python commands through the managed environment with `uv run`:

```bash
uv run python --version
```

### Configuration

The application loads configuration from environment variables. For local development,
copy `.env.example` to `.env` and adjust the values as needed:

```bash
cp .env.example .env
```

The `.env` file is ignored by Git and must not contain values that should be committed.
Environment variables use the `STRUMSPACE_` prefix. The application uses
`Asia/Kolkata` as its default project timezone.

### Run tests

```bash
uv run pytest
```
