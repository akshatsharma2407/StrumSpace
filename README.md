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
root account. The test database and test user are configured separately through
the `STRUMSPACE_TEST_DATABASE_*` variables described below.

The development database remains isolated from the test database. Test execution
must never use the development database credentials.

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

Tests use a dedicated MySQL database and user. Create them from a MySQL
administrative account, using a test-only password:

```sql
CREATE DATABASE strumspace_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'strumspace_test_user'@'localhost' IDENTIFIED BY 'YOUR_TEST_DATABASE_PASSWORD';
GRANT ALL PRIVILEGES ON strumspace_test.* TO 'strumspace_test_user'@'localhost';
FLUSH PRIVILEGES;
```

Set the `STRUMSPACE_TEST_DATABASE_*` variables in your local environment. The
test database name and user must differ from the development database and user.
Apply migrations to the test database explicitly, then run:

```bash
uv run alembic upgrade head
uv run pytest
```

Database tests verify `SELECT DATABASE()` and fail when test configuration would
point at the development database. Tests must never be run with development
database credentials in the `STRUMSPACE_TEST_DATABASE_*` variables.

### Database migrations

Alembic manages database schema versioning. Migration configuration reuses the
application database settings from `.env`; credentials are not stored in
`alembic.ini`.

Create and review an autogenerated migration after changing SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe the schema change"
```

Apply migrations, inspect the current revision or history, and downgrade one
revision with:

```bash
uv run alembic upgrade head
uv run alembic current
uv run alembic history
uv run alembic downgrade -1
```

Autogenerated migrations must be reviewed before they are applied. The current
baseline intentionally contains no academy-specific tables; those will be added
alongside future feature modules.
