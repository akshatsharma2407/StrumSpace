# Phase 1 — Backend Foundation

**Phase:** 1

**Milestone:** M1 — Backend Foundation

**Status:** In Progress

**Start Date:** 24 November 2026

**Previous Phase:** Phase 0 — Product Discovery & Architecture (Completed)

---

## 1. Phase Objective

Establish a reliable, maintainable, and testable backend foundation for StrumSpace.

This phase focuses on application infrastructure, development environment, configuration management, database connectivity, migrations, logging, error handling, and testing infrastructure.

No academy-specific business functionality will be implemented during this phase.

By the end of Phase 1, the project should have a working backend environment upon which subsequent functional modules can be developed.

---

## 2. Reference Documents

Before planning or implementing any task, refer to the relevant project documentation:

- `CLAUDE.md` — Project-wide development instructions.
- `docs/PRD.md` — Product requirements and scope.
- `docs/decisions/ADR-001.md` — Architecture and engineering decisions.
- `docs/DEVELOPMENT-MILESTONES.md` — Development roadmap.
- `.claude/phases/phase-0.md` — Previous phase decisions and completion record.

Implementation must remain consistent with the agreed architectural decisions.

Any proposed deviation must be discussed and approved before implementation.

---

## 3. Development Tasks

### Task 1.1 — Project Initialization

**Status:** Completed

Establish the Python development environment and initial project structure.

**Scope:**

- Decide the Python version.
- Select the package and dependency management approach.
- Configure the virtual environment.
- Establish dependency definitions.
- Create the minimum required application directory structure.
- Configure `.gitignore`.
- Establish development dependencies.

**Acceptance Criteria:**

- [x] Python version is explicitly defined.
- [x] Dependency management approach is documented.
- [x] Development environment can be reproduced.
- [x] Required dependencies can be installed successfully.
- [x] Initial project structure follows the agreed architecture.
- [x] Environment files and generated artifacts are appropriately ignored by Git.

---

### Task 1.2 — FastAPI Application Foundation

**Status:** Completed

Initialize the FastAPI application and establish the basic application lifecycle.

**Scope:**

- Create the FastAPI application entry point.
- Configure application metadata.
- Establish API versioning.
- Configure the initial router structure.
- Establish application lifespan management where required.
- Implement a basic health-check endpoint.
- Verify Swagger and OpenAPI documentation.

**Acceptance Criteria:**

- [x] FastAPI application starts successfully.
- [x] Application entry point is clearly defined.
- [x] API versioning follows ADR-001.
- [x] Health-check endpoint returns a successful response.
- [x] Swagger documentation is accessible.
- [x] Application startup and shutdown work correctly.

---

### Task 1.3 — Configuration Management

**Status:** Completed

Establish centralized and environment-based application configuration.

**Scope:**

- Configure application settings using Pydantic Settings.
- Establish environment variable management.
- Create `.env.example`.
- Separate sensitive configuration from source code.
- Define configuration validation.
- Establish IST (`Asia/Kolkata`) as the application timezone convention.

**Acceptance Criteria:**

- [x] Application configuration is centrally managed.
- [x] Settings can be loaded from environment variables.
- [x] Required configuration values are validated.
- [x] Sensitive credentials are not committed to Git.
- [x] `.env.example` documents required environment variables.
- [x] Timezone configuration follows ADR-001.

---

### Task 1.4 — Local MySQL Infrastructure

**Status:** Completed

Establish a local MySQL database environment for application development.

**Scope:**

- Select an appropriate MySQL version.
- Install and configure MySQL on the local machine, if not already installed.
- Create the StrumSpace development database.
- Create a dedicated database user and configure appropriate privileges.
- Configure database credentials through environment variables.
- Verify local database connectivity.
- Document the local database setup process.

**Acceptance Criteria:**

- [x] MySQL server is installed and running locally.
- [x] StrumSpace development database is created.
- [x] Dedicated database user is configured with appropriate privileges.
- [x] Database credentials are externally configured.
- [x] Database connectivity is verified using the configured credentials.
- [x] Local database setup instructions are documented.

**Note:** Docker and Docker Compose implementation for both the backend and database is intentionally deferred until M10 — Hardening & Production Readiness. Application-level database integration will be implemented separately in Task 1.5.

---

### Task 1.5 — Async Database Integration

**Status:** Pending

Integrate the FastAPI application with MySQL using SQLAlchemy's asynchronous database interface.

**Scope:**

- Configure SQLAlchemy 2.x.
- Configure the `asyncmy` database driver.
- Establish the asynchronous database engine.
- Configure connection pooling.
- Configure `AsyncSession` and session factories.
- Establish request-scoped database session management.
- Define the transaction management approach.
- Handle database connection lifecycle.
- Verify database connectivity.

**Acceptance Criteria:**

- [ ] Application connects to MySQL successfully.
- [ ] Database operations support asynchronous execution.
- [ ] Database sessions are properly created and closed.
- [ ] Request-scoped session dependencies are available.
- [ ] Connection pooling is configured appropriately.
- [ ] Transaction and rollback behavior is understood and established.
- [ ] Database resources are released correctly during application shutdown.

---

### Task 1.6 — Database Migration Infrastructure

**Status:** Pending

Establish database schema versioning using Alembic.

**Scope:**

- Initialize Alembic.
- Configure Alembic for the asynchronous SQLAlchemy setup.
- Integrate migration configuration with application settings.
- Establish SQLAlchemy model metadata.
- Define migration naming and execution conventions.
- Verify migration infrastructure.

**Acceptance Criteria:**

- [ ] Alembic is initialized successfully.
- [ ] Alembic can connect to the configured MySQL database.
- [ ] SQLAlchemy metadata is accessible to Alembic.
- [ ] Migration generation and execution workflows are verified.
- [ ] Migration upgrade and downgrade procedures are understood.
- [ ] No unnecessary business entities or placeholder tables are introduced.

---

### Task 1.7 — Logging & Error Handling

**Status:** Pending

Establish consistent application logging and exception handling.

**Scope:**

- Configure application logging.
- Establish configurable log levels.
- Define a consistent log format.
- Establish application-level exception handling.
- Define reusable application exceptions where appropriate.
- Standardize API error responses according to ADR-001.
- Handle request validation errors consistently.
- Prevent exposure of sensitive internal error details.

**Acceptance Criteria:**

- [ ] Application logging is centrally configured.
- [ ] Log levels can be configured.
- [ ] Application errors are handled consistently.
- [ ] API error responses follow the agreed format.
- [ ] Validation errors are handled appropriately.
- [ ] Unexpected errors are logged without exposing sensitive details to API consumers.

---

### Task 1.8 — Testing Infrastructure & Foundation Verification

**Status:** Pending

Establish the testing environment and verify the complete backend foundation.

**Scope:**

- Configure pytest.
- Configure pytest-asyncio.
- Configure HTTPX for API testing.
- Establish the initial test directory structure.
- Configure an isolated MySQL test database.
- Establish reusable test fixtures.
- Test the health-check endpoint.
- Test database connectivity and session behavior.
- Verify application configuration and error handling.
- Review the complete foundation.

**Acceptance Criteria:**

- [ ] Tests can be executed using a documented command.
- [ ] Asynchronous tests are supported.
- [ ] API endpoints can be tested using HTTPX.
- [ ] Test database is isolated from the development database.
- [ ] Health-check tests pass.
- [ ] Database connectivity tests pass.
- [ ] Relevant configuration and error-handling tests pass.
- [ ] Test execution does not modify development data.
- [ ] Backend foundation has been reviewed and approved.

---

## 4. Implementation Workflow

Every task must follow the workflow below.

### Step 1 — Understand

Discuss the purpose of the task, relevant concepts, requirements, and available technical approaches.

### Step 2 — Plan

Inspect the existing repository and prepare an implementation plan covering:

- Proposed changes.
- Files to create or modify.
- Required dependencies.
- Technical reasoning.
- Potential trade-offs.
- Verification approach.

### Step 3 — Approval

Present the implementation plan to the project owner.

Do not begin implementation until the plan is explicitly approved.

### Step 4 — Implement

Implement only the approved task and scope.

Avoid unrelated refactoring, unnecessary abstractions, and premature implementation of future tasks.

### Step 5 — Verify

Execute relevant tests and verification commands.

Report:

- Changes made.
- Files created or modified.
- Verification results.
- Known limitations.
- Any remaining concerns.

### Step 6 — Review & Close

The project owner reviews the implementation, understands the technical decisions, and approves task completion.

Update the task status and acceptance criteria only after verification and approval.

Do not automatically proceed to the next task.

---

## 5. Implementation Boundaries

During Phase 1, do not implement:

- Enquiry management.
- Trial class booking.
- Student management.
- Batch and enrollment management.
- Attendance management.
- Fee and payment management.
- Notifications or background workers.
- Authentication and authorization.
- Frontend functionality.
- Business-specific database entities.
- A complete database schema or ERD.
- Docker and Docker Compose (including backend and database containerization).
- Production deployment infrastructure.

Only introduce infrastructure and abstractions that are necessary for the current phase.

Do not create empty feature modules merely to represent future functionality.

---

## 6. Engineering Requirements

All implementation must follow the architectural decisions documented in ADR-001.

In particular:

- Maintain a modular monolith architecture.
- Use asynchronous programming for appropriate I/O-bound operations.
- Use MySQL as the primary database.
- Use SQLAlchemy 2.x with `asyncmy`.
- Use Alembic for database migrations.
- Follow the agreed REST API conventions.
- Maintain IST as the application timezone convention.
- Keep configuration and credentials outside source code.
- Maintain clear separation of responsibilities.
- Avoid premature optimization and unnecessary complexity.
- Write meaningful tests.
- Keep implementation readable and understandable.

---

## 7. Progress Tracker

| Task | Description | Status |
|---|---|---|
| 1.1 | Project Initialization | Completed |
| 1.2 | FastAPI Application Foundation | Completed |
| 1.3 | Configuration Management | Completed |
| 1.4 | Local MySQL Infrastructure | Completed |
| 1.5 | Async Database Integration | Pending |
| 1.6 | Database Migration Infrastructure | Pending |
| 1.7 | Logging & Error Handling | Pending |
| 1.8 | Testing Infrastructure & Foundation Verification | Pending |

**Current Active Task:** 1.5 — Async Database Integration

**Completed Tasks:** 4/8

**Completed Task:** 1.4 — Local MySQL Infrastructure

---

## 8. Phase 1 Exit Criteria

Phase 1 can be considered complete when:

- [ ] All Phase 1 tasks are completed and approved.
- [ ] The development environment is reproducible.
- [ ] FastAPI application runs successfully.
- [ ] Local MySQL infrastructure is operational.
- [ ] FastAPI and MySQL run directly on the local machine without Docker.
- [ ] Async database connectivity and session management are functional.
- [ ] Alembic migration infrastructure is operational.
- [ ] Configuration and secrets are managed appropriately.
- [ ] Logging and error handling are established.
- [ ] Testing infrastructure is operational.
- [ ] All relevant tests pass.
- [ ] Required documentation is updated.
- [ ] Implementation has been reviewed by the project owner.
- [ ] Phase 1 receives explicit final approval.

---

## 9. Handoff to Phase 2

After successful completion and approval of Phase 1, the project will move to:

**Phase 2 — Enquiry Management (M2)**

Phase 2 will introduce the first business-specific module, including database entity modeling, ERD updates, API design, business logic, and feature-specific testing.

Do not begin Phase 2 without explicit approval.

---

## 10. Guiding Principle

Build a strong foundation without attempting to anticipate every future requirement.

The objective is not simply to make the application run, but to understand how its infrastructure works, why each component exists, and how subsequent features will build upon it.
