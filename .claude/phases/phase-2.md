# Phase 2 — Enquiry Management

**Phase:** 2  
**Milestone:** M2 — Enquiry Management  
**Status:** Planned — Ready for Review  
**Previous Phase:** Phase 1 — Backend Foundation (Completed)  
**Primary Module:** `app/modules/enquiries/`

---

## 1. Phase Objective

Build the first business-specific module in StrumSpace: a reliable API for recording, maintaining, tracking, and retrieving prospective-student enquiries.

By the end of this phase, academy staff should be able to manage enquiry records through the versioned REST API instead of relying on scattered manual records. The module will establish feature-oriented structure, database modeling, validation, transaction management, and testing patterns that later modules can reuse.

This phase introduces enquiry functionality only. Trial booking and enquiry-to-student conversion will be implemented in their respective future milestones.

---

## 2. Reference Documents and Existing Foundation

Before planning or implementing a task, review the relevant project documentation and existing implementation:

- `CLAUDE.md` — Project instructions and approval workflow.
- `docs/PRD.md` — Product requirements and enquiry workflow.
- `docs/decisions/ADR-001.md` — Architecture, API, database, timezone, and testing standards.
- `docs/decisions/development-milestones.md` — M2 deliverables and milestone outcome.
- `.claude/phases/phase-0.md` — Planning decisions and incremental modeling strategy.
- `.claude/phases/phase-1.md` — Completed backend foundation.
- Existing code under `app/` — Configuration, database sessions, exception handling, and router registration.
- Existing tests under `tests/` — Async API tests and isolated MySQL test fixtures.

Reuse the Phase 1 foundation. Do not introduce parallel configuration, database session, error-handling, or testing infrastructure unnecessarily.

Any deviation from the agreed architecture or phase plan must be discussed and approved before implementation.

---

## 3. Scope and Business Decisions

### Included

- Create, retrieve, list, and partially update enquiries.
- Maintain prospective-student contact and enquiry information.
- Track enquiry statuses and enforce approved transitions.
- Record follow-up information needed for the current workflow.
- Support filtering, basic search, deterministic sorting, and limit/offset pagination.
- Handle duplicate or repeated enquiries according to an approved policy.
- Implement relevant input validation, database constraints, indexes, and transaction boundaries.
- Update the ERD and maintain meaningful unit, integration, and API tests.

### Excluded

- Trial class availability and booking (M3).
- Student creation and enquiry-to-student conversion (M4).
- Batch, attendance, and payment management.
- Notifications, email/SMS/WhatsApp integrations, and background jobs (M8).
- Authentication, authorization, and role checks (M9).
- Frontend functionality and Docker containerization.
- Advanced search infrastructure, assignment workflows, audit history, and soft deletion unless a reviewed M2 requirement justifies them.
- Speculative entities, endpoints, or abstractions for future features.

Until authentication and authorization are implemented, the enquiry API is for local development only. Do not expose it publicly or use real prospective-student personal data in development or testing.

### Decisions to Make During the Phase

The following must be discussed and approved during the relevant tasks rather than assumed by the implementation assistant:

- Exact enquiry fields and required versus optional information.
- Initial status, status vocabulary, terminal statuses, and allowed transitions.
- What constitutes a duplicate or repeated enquiry and how it should be handled.
- Minimum follow-up information and whether it belongs on the enquiry itself.
- Allowed updates, restricted fields, and validation rules.
- Supported filters, search fields, sort fields, and default ordering.
- How closed enquiries remain accessible and how future workflows can reference an enquiry without implementing those workflows now.

Record approved decisions in the relevant task plan and documentation. No separate extensive discovery document is required.

---

## 4. Proposed Module and API Direction

The proposed module structure follows ADR-001:

```text
app/
└── modules/
    └── enquiries/
        ├── __init__.py
        ├── models.py
        ├── schemas.py
        ├── repository.py
        ├── service.py
        └── router.py
```

Create files incrementally as they become necessary. Routers handle HTTP concerns, schemas define API contracts, services enforce business rules and transaction boundaries, repositories perform persistence operations, and models represent database structures.

### Proposed Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/enquiries` | Create an enquiry |
| GET | `/api/v1/enquiries` | List enquiries |
| GET | `/api/v1/enquiries/{enquiry_id}` | Retrieve an individual enquiry |
| PATCH | `/api/v1/enquiries/{enquiry_id}` | Partially update an enquiry |

Exact request and response fields, status codes, query parameters, and transition semantics will be reviewed in Task 2.3.

Follow ADR-001 conventions, including snake_case JSON fields, standardized errors, and limit/offset pagination. Collection responses will contain `items`, `total`, `limit`, and `offset`, where `total` is the exact count of records matching the filters before pagination. Use a straightforward count query rather than premature optimization.

Do not introduce separate action-style, deletion, follow-up, or conversion endpoints unless an approved requirement justifies them.

---

## 5. Development Tasks

### Task 2.1 — Enquiry Domain Discovery and Business Rules

**Status:** Completed  
**Depends on:** Phase 1 completion

Understand the actual enquiry workflow before designing tables or endpoints.

**Scope:**

- Translate the PRD and M2 requirements into concrete enquiry use cases.
- Identify required and optional contact, source, interest, notes, and follow-up information.
- Define the enquiry lifecycle and allowed status transitions.
- Define duplicate/repeated-enquiry handling and normalization requirements.
- Identify validation rules, update behavior, and data integrity requirements.
- Identify which rules belong in the application and which need database enforcement.
- Record approved decisions and any remaining questions.

**Acceptance Criteria:**

- [x] Enquiry use cases and non-goals are understood and documented.
- [x] Required and optional information is identified.
- [x] Status vocabulary and allowed transitions are approved.
- [x] Duplicate/repeated-enquiry policy is approved.
- [x] Follow-up scope is defined without introducing a notification or CRM subsystem.
- [x] Validation, integrity, and transaction requirements are identified.
- [x] No future-module behavior is included prematurely.

**Verification:** Review and approve the business rules before proceeding to database design.

---

### Task 2.2 — Enquiry Data Model and ERD

**Status:** Not Started  
**Depends on:** Task 2.1

Design the minimum relational model required by the approved enquiry workflow. This is a design task; model and migration implementation belongs to Task 2.4.

**Scope:**

- Define the enquiry entity, columns, MySQL-compatible data types, nullability, defaults, and timestamps.
- Decide status representation and any normalized contact fields required by the duplicate policy.
- Define relevant uniqueness, foreign-key, check-constraint, and index requirements.
- Decide whether follow-up information requires a separate entity; introduce one only if justified by the approved requirements.
- Update the incremental ERD/database documentation.
- Identify any migration considerations without generating or executing migrations.

**Acceptance Criteria:**

- [ ] The proposed model supports all approved M2 data requirements.
- [ ] Columns, types, constraints, and indexes are explicitly defined and justified.
- [ ] Timestamp interpretation follows the IST convention in ADR-001.
- [ ] The ERD reflects the approved model and does not introduce speculative entities or relationships.
- [ ] The database design is reviewed and approved before implementation.

**Verification:** Review the proposed schema and ERD against the approved domain rules.

---

### Task 2.3 — Enquiry Schemas and API Contract

**Status:** Not Started  
**Depends on:** Tasks 2.1 and 2.2

Define the public API contract and implement the corresponding Pydantic schemas.

**Scope:**

- Define create, partial-update, and response schemas.
- Define path and query parameter validation.
- Define the supported filters, basic search, sort fields, sort direction, limit, and offset.
- Establish deterministic ordering, with a tie-breaker where needed.
- Define successful responses and standardized validation, not-found, duplicate, and invalid-transition errors.
- Define partial-update semantics, including omitted fields versus explicit null values.
- Ensure datetime interpretation and serialization follow the IST convention in ADR-001.
- Write focused schema validation tests.

**Acceptance Criteria:**

- [ ] Request and response fields and their validation rules are explicit and approved.
- [ ] URL paths, JSON naming, pagination, and error contracts follow ADR-001.
- [ ] Unsupported filters, sort fields, and invalid query values have defined rejection behavior.
- [ ] Partial updates have clearly defined semantics.
- [ ] Schema-level tests cover meaningful valid, invalid, and boundary inputs.

**Verification:** Review the API contract and run schema-level tests. Verify generated OpenAPI and actual HTTP behavior in Task 2.7, after the routes exist.

---

### Task 2.4 — Enquiry Model, Alembic Migration, and Database Integration

**Status:** Not Started  
**Depends on:** Tasks 2.2 and 2.3

Implement the approved database design using the existing Phase 1 SQLAlchemy and Alembic infrastructure.

**Scope:**

- Implement the SQLAlchemy model and register it with the existing model metadata.
- Ensure Alembic can discover the model without introducing import cycles.
- Generate and review the migration before applying it.
- Maintain one Alembic configuration and one migration history for development and testing.
- Establish a simple, documented way to target the isolated MySQL test database using the existing migration setup.
- Verify the test database identity and dedicated test user before migration or destructive test operations; fail safely if the target is incorrect.
- Apply the migration to the test database and verify schema, constraints, indexes, defaults, persistence, downgrade, and re-upgrade behavior.
- After successful verification and owner approval, apply the same migration to the development database.
- Keep unrelated foundation behavior unchanged.

**Acceptance Criteria:**

- [ ] The model and reviewed migration match the approved database design.
- [ ] The migration upgrades successfully against the isolated test database.
- [ ] Valid records persist and reload correctly; relevant constraints reject invalid records.
- [ ] Downgrade and re-upgrade work on the test database and affect only the intended objects.
- [ ] The approved migration is applied successfully to the development database.
- [ ] Both databases use the same migration history with independent revision states.
- [ ] Test setup is protected against accidental use of the development database.
- [ ] Migration setup and execution commands are documented.

**Verification:** Inspect the migration and actual schema, run focused database tests, and verify Alembic revision state in both databases. Perform downgrade verification only against the isolated test database.

---

### Task 2.5 — Enquiry Repository

**Status:** Not Started  
**Depends on:** Task 2.4

Implement focused asynchronous persistence operations for enquiries.

**Scope:**

- Implement create, retrieve-by-ID, list, and update operations.
- Implement duplicate-detection queries according to the approved policy.
- Implement supported filters, search, sorting, pagination, and exact filtered total calculation.
- Use the existing request-scoped `AsyncSession`.
- Keep query construction and persistence details out of routers.
- Avoid implicit commits; respect the transaction strategy established in Phase 1 and the service layer.
- Avoid unnecessary generic repository abstractions.

**Acceptance Criteria:**

- [ ] Repository operations use asynchronous SQLAlchemy APIs correctly.
- [ ] Queries return the expected records, counts, and deterministic ordering.
- [ ] Filters, search, and pagination behave correctly, including empty results and boundaries.
- [ ] Duplicate lookup matches the approved business policy.
- [ ] Repository operations follow the agreed transaction ownership model.
- [ ] Focused repository integration tests pass against MySQL.

**Verification:** Run repository integration tests against the isolated test database and inspect query behavior where necessary.

---

### Task 2.6 — Enquiry Service and Business Rules

**Status:** Not Started  
**Depends on:** Tasks 2.1 and 2.5

Implement the approved business workflows independently of HTTP details.

**Scope:**

- Implement enquiry creation, normalization, and duplicate/repeated-enquiry handling.
- Implement retrieval and listing orchestration.
- Implement partial updates, allowed status transitions, and restricted-field rules.
- Establish explicit transaction boundaries consistent with the database session management implemented in Phase 1.
- Keep multi-step writes atomic and handle rollback correctly.
- Enforce database-backed integrity rules and handle relevant uniqueness races or concurrent updates according to the approved policy.
- Translate expected failures into safe, standardized application exceptions.
- Keep trial booking and student conversion outside this service.

**Acceptance Criteria:**

- [ ] Approved business rules and status transitions are enforced consistently.
- [ ] Duplicate/repeated enquiries produce the approved outcome.
- [ ] Retrieve and update operations handle missing records consistently.
- [ ] Invalid updates and transitions produce the agreed application errors.
- [ ] Multi-step writes are atomic and roll back on failure.
- [ ] Relevant database conflicts and concurrent operations preserve the approved integrity rules without leaking internals.
- [ ] Focused service unit tests pass.

**Verification:** Run service tests for approved rules and relevant failure scenarios; verify actual transaction and concurrency behavior using database integration tests where needed.

---

### Task 2.7 — Enquiry API Routes and Router Integration

**Status:** Not Started  
**Depends on:** Tasks 2.3 and 2.6

Expose the approved enquiry functionality through the versioned FastAPI application.

**Scope:**

- Implement create, retrieve, list, and partial-update routes.
- Inject the existing request-scoped database session dependency.
- Keep route handlers thin and delegate business behavior to the service.
- Register the enquiries router in the existing v1 router.
- Return the approved status codes and response schemas.
- Integrate with the existing standardized error handlers.
- Verify Swagger/OpenAPI documentation, query parameters, and HTTP responses against the approved contract.

**Acceptance Criteria:**

- [ ] All approved enquiry endpoints are accessible at their intended paths.
- [ ] Successful HTTP responses and error responses match the API contract.
- [ ] Filtering, search, sorting, and pagination work through the API.
- [ ] Route handlers reuse the agreed module boundaries and dependencies.
- [ ] OpenAPI documentation accurately describes the implemented API.
- [ ] Existing health endpoint and foundation behavior remain unchanged.
- [ ] Focused API integration tests pass using HTTPX.

**Verification:** Run API tests, inspect Swagger/OpenAPI, and manually verify the principal workflows where useful.

---

### Task 2.8 — Enquiry Testing and Failure-Scenario Coverage

**Status:** Not Started  
**Depends on:** Tasks 2.4–2.7

Consolidate the tests introduced during implementation and fill meaningful coverage gaps rather than rewriting existing tests.

**Scope:**

- Review unit tests for normalization, validation, status transitions, and duplicate policy.
- Review MySQL integration tests for persistence, constraints, migrations, transaction rollback, and relevant concurrency behavior.
- Review HTTPX tests for create, retrieve, list, update, filtering, search, sorting, pagination, and standardized errors.
- Cover relevant edge cases, including invalid transitions, not-found records, duplicate requests, omitted versus null fields, and empty results.
- Ensure test data is isolated between tests and cleanup cannot affect the development database.
- Use the shared Alembic migration history to keep the test schema current through a simple documented setup; automate only what is useful.
- Run the complete test suite, including Phase 1 tests.

**Acceptance Criteria:**

- [ ] Core M2 workflows and meaningful failure paths are covered by appropriate tests.
- [ ] Approved business rules, data constraints, and relevant boundary behavior are verified.
- [ ] Database transaction rollback and applicable race/constraint behavior are verified on MySQL.
- [ ] Tests are repeatable, with documented setup and execution commands.
- [ ] Automated tests do not use or modify development data.
- [ ] The complete test suite passes without regressing Phase 1 behavior.

**Verification:** Run the documented full test command and any focused integration or migration checks needed to verify the remaining gaps.

---

### Task 2.9 — Documentation, Review, and Phase Closure

**Status:** Not Started  
**Depends on:** Tasks 2.1–2.8

Review the implemented module and formally close Phase 2 after owner approval.

**Scope:**

- Update the phase progress tracker and relevant documentation to match the implementation.
- Ensure the ERD, approved business rules, and API contract reflect actual behavior.
- Update README or setup instructions if migration, testing, or API usage has changed.
- Review module boundaries, query behavior, error handling, and migration quality.
- Record any relevant handoff considerations for M3 and M4 without implementing those features.
- Confirm no speculative abstractions or unrelated functionality have been introduced.

**Acceptance Criteria:**

- [ ] Documentation reflects the implemented module.
- [ ] Database migration and test setup instructions are current.
- [ ] The final implementation meets the approved M2 requirements.
- [ ] No known high-severity data-integrity or API-contract issue remains open.
- [ ] The project owner understands the implementation and its technical decisions.
- [ ] The project owner explicitly approves Phase 2 completion.

**Verification:** Review the final diff and verification results, resolve blocking issues, and obtain explicit approval.

---

## 6. Implementation Workflow

Every task follows the established project workflow:

1. **Understand** — Discuss requirements, concepts, and assumptions.
2. **Inspect** — Review the relevant existing code, migrations, tests, and documentation.
3. **Plan** — Propose focused changes, affected files, technical reasoning, and verification steps.
4. **Approve** — Obtain explicit owner approval before implementation.
5. **Implement** — Implement only the approved task and scope.
6. **Verify** — Run relevant checks and report actual results, changes, and limitations.
7. **Review and close** — Obtain owner approval, update task status and acceptance criteria, and stop before the next task.

Discussing a possible field, rule, endpoint, or technical approach does not constitute approval to implement it. Avoid unrelated refactoring and unnecessary dependencies. Do not automatically begin the next task or commit changes without owner approval.

---

## 7. Testing and Verification Strategy

Follow the existing layered testing strategy from ADR-001:

- **Unit tests:** Schema validation and business rules in isolation.
- **Integration tests:** Persistence, database constraints, queries, migrations, transaction management, and relevant concurrency behavior using the isolated MySQL test database.
- **API/end-to-end tests:** Complete enquiry workflows and meaningful HTTP success and failure scenarios through HTTPX.

Write focused tests alongside implementation. Task 2.8 consolidates coverage and verifies the complete suite. Prioritize useful tests over arbitrary coverage targets or requiring a failure test for every individual deliverable.

Development and test databases and credentials must remain separate. Use the existing dedicated test user and verify the test target before destructive operations. Do not introduce a second Alembic migration history or configuration.

---

## 8. Progress Tracker

| Task | Description | Status |
|---|---|---|
| 2.1 | Enquiry Domain Discovery and Business Rules | Completed |
| 2.2 | Enquiry Data Model and ERD | Not Started |
| 2.3 | Enquiry Schemas and API Contract | Not Started |
| 2.4 | Enquiry Model, Alembic Migration, and Database Integration | Not Started |
| 2.5 | Enquiry Repository | Not Started |
| 2.6 | Enquiry Service and Business Rules | Not Started |
| 2.7 | Enquiry API Routes and Router Integration | Not Started |
| 2.8 | Enquiry Testing and Failure-Scenario Coverage | Not Started |
| 2.9 | Documentation, Review, and Phase Closure | Not Started |

**Next Task:** 2.2 — Enquiry Data Model and ERD  
**Current Active Task:** 2.2 — awaiting approval.  
**Completed Tasks:** 1/9

---

## 9. Phase 2 Exit Criteria

- [ ] All approved Phase 2 tasks are completed and reviewed.
- [ ] Enquiries can be created, retrieved, listed, and partially updated through the API.
- [ ] Approved status transitions, follow-up behavior, validation, and duplicate/repeated-enquiry rules work correctly.
- [ ] Filtering, search, sorting, and pagination follow the approved contract.
- [ ] Database model, ERD, constraints, indexes, and migrations are reviewed and verified.
- [ ] Development and test schemas are current and test execution cannot modify development data.
- [ ] Standardized errors do not expose internal implementation details.
- [ ] Meaningful unit, integration, and API tests pass, including Phase 1 regression tests.
- [ ] Documentation reflects the actual implementation.
- [ ] The project owner understands the module and explicitly approves Phase 2 completion.

---

## 10. Handoff to Phase 3

After Phase 2 completion and approval, proceed to **Phase 3 — Trial Class Booking (M3)**.

Preserve the approved enquiry identifier and relevant lifecycle semantics so the booking module can associate trial bookings with enquiries without unnecessary coupling.

Do not implement trial booking as part of Phase 2 or begin Phase 3 without explicit approval.

---

## 11. Guiding Principle

Implement the smallest complete enquiry workflow that satisfies M2, protects data integrity, and establishes understandable patterns for later modules.

Prefer explicit, practical decisions and incremental implementation over speculative CRM features, premature abstractions, and unnecessary documentation.
