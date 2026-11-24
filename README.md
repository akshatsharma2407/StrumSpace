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

### Local MySQL development

StrumSpace uses **MySQL 8.4 LTS** as its local development database. Install MySQL
locally and ensure the server is running on port `3307` (or update the values in
`.env`). Docker is not part of the current development workflow.

Create the StrumSpace development database and a dedicated application user
from a MySQL administrative account:

```sql
CREATE DATABASE strumspace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'strumspace_user'@'localhost' IDENTIFIED BY 'YOUR_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON strumspace.* TO 'strumspace_user'@'localhost';
FLUSH PRIVILEGES;
```

Use a different password in a real local environment and set the same value in
`.env` as `STRUMSPACE_DATABASE_PASSWORD`. The application must not use the MySQL
root account. A separate test database and test user will be introduced with the
testing infrastructure in Task 1.8.

To verify the application credentials manually:

```bash
mysql -h localhost -P 3307 -u strumspace_app -p strumspace
```

To verify that the configured user has access to the development database, run
`SELECT DATABASE();` after connecting and confirm it returns `strumspace`.

To verify connectivity with the application itself, use the database connection
verification implemented in Task 1.5. The application creates an asynchronous
SQLAlchemy engine using the `mysql+asyncmy` driver, checks the database during
startup, and disposes its connection pool during shutdown.

The database pool can be tuned through `STRUMSPACE_DATABASE_POOL_SIZE`,
`STRUMSPACE_DATABASE_MAX_OVERFLOW`, `STRUMSPACE_DATABASE_POOL_TIMEOUT`, and
`STRUMSPACE_DATABASE_POOL_RECYCLE`. Set `STRUMSPACE_DATABASE_ECHO=true` only
when SQL statement logging is needed during local development.

For a direct connectivity check, run:

```bash
uv run python -c "import asyncio; from app.db.engine import verify_database_connection; asyncio.run(verify_database_connection())"
```

Database-backed routes can request a request-scoped session through the
`get_db_session` dependency from `app.db.dependencies`. The dependency closes
the session after each request. Services should define explicit transaction
boundaries with `async with session.begin():`; the dependency does not commit
implicitly.

If the database is unavailable, application startup fails rather than starting
an instance that cannot perform database operations.


Database connectivity is not claimed as verified by this setup documentation
until MySQL is installed locally and the Task 1.5 integration check succeeds.

The task's MySQL setup is intentionally local-only. Docker and Docker Compose are
deferred until M10, as documented in the phase plan.

The local setup is complete when MySQL is running, the `strumspace` database
exists, and `strumspace_app` can connect with the credentials in `.env`.

Start and stop the MySQL service using the service manager provided by the local
MySQL installation. Stopping and restarting the service preserves database data;
resetting a database should be an explicit administrative operation.

The application settings validate database identifiers, the port, host, and
non-empty passwords. Database engine and session configuration will be added in
Task 1.5.

The application settings validate database identifiers, the port, host, and
non-empty passwords. Database engine and session configuration will be added in
Task 1.5.

### Run tests

```bash
uv run pytest
```
