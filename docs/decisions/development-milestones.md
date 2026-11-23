# StrumSpace — Development Milestones

## Overview

This document defines the planned development milestones for StrumSpace, a backend-focused Guitar Academy Management System.

Development will follow an incremental approach. Each milestone will deliver a functional part of the system, with its implementation details, database schema, APIs, business rules, and tests defined when that milestone begins.

The goal is to build a maintainable, reliable, and industry-oriented backend without introducing unnecessary complexity or designing features prematurely.

---

## M1 — Backend Foundation

Establish the core application infrastructure and development environment.

**Key deliverables**
- Initialize the FastAPI application structure.
- Configure project dependencies and environment management.
- Set up configuration and environment variables.
- Implement logging and application-level error handling foundations.
- Set up MySQL with Docker and Docker Compose.
- Configure SQLAlchemy async database connectivity and session management.
- Initialize Alembic for database migrations.
- Establish the testing infrastructure.
- Implement a basic health-check endpoint.

**Milestone outcome:** A running backend with a working database connection, migration infrastructure, and a foundation for developing features.

---

## M2 — Enquiry Management

Build the system for managing prospective students and their enquiries.

**Key deliverables**
- Create and manage enquiries.
- Retrieve individual enquiries and list enquiries.
- Update enquiry information.
- Track enquiry statuses.
- Implement validation and relevant business rules.
- Support filtering and pagination.
- Handle duplicate or repeated enquiries appropriately.

**Milestone outcome:** Enquiries can be managed and tracked through the API instead of relying on scattered manual records.

---

## M3 — Trial Class Booking

Implement the trial class scheduling and booking system.

**Key deliverables**
- Manage trial booking information.
- Define and manage availability as required.
- Book and cancel trial classes.
- Handle scheduling conflicts.
- Prevent double-booking and race conditions.
- Maintain transactional integrity.
- Validate booking rules and relevant status transitions.

**Milestone outcome:** A reliable trial booking system that can handle concurrent requests and prevent conflicting bookings.

---

## M4 — Student Management

Build the student record management system.

**Key deliverables**
- Convert eligible enquiries into student records.
- Create and maintain student profiles.
- Retrieve individual student records and student lists.
- Update student information.
- Manage student lifecycle/status.
- Maintain data integrity during enquiry-to-student conversion.

**Milestone outcome:** A centralized system for managing students and their records.

---

## M5 — Batch & Enrollment Management

Implement batch creation, scheduling, and student enrollment.

**Key deliverables**
- Create and manage batches.
- Define batch schedules.
- Manage batch capacity.
- Enroll students into batches.
- Handle enrollment changes and removals.
- Validate scheduling conflicts and enrollment constraints.

**Milestone outcome:** Students can be organized into batches with controlled enrollment and scheduling.

---

## M6 — Attendance Management

Build the attendance tracking system for academy classes.

**Key deliverables**
- Record attendance for scheduled classes.
- Track attendance statuses.
- Update or correct attendance records.
- Retrieve attendance history.
- Generate student-level attendance summaries.
- Generate batch-level attendance summaries.
- Enforce attendance-related business rules.

**Milestone outcome:** The academy can maintain accurate attendance records and review attendance history.

---

## M7 — Fee & Payment Management

Implement basic financial record management for student fees and payments.

**Key deliverables**
- Maintain fee-related records.
- Record student payments.
- Track payment dates and amounts.
- Retrieve payment history.
- Calculate outstanding balances where applicable.
- Handle payment record corrections according to defined rules.

**Milestone outcome:** The academy can track payment records, received amounts, and outstanding fees.

*Note: This milestone focuses on internal payment record management, not payment gateway integration.*

---

## M8 — Notifications & Background Jobs

Introduce asynchronous background processing for tasks that should not depend on an API request remaining active.

**Key deliverables**
- Identify tasks requiring background execution.
- Implement background job processing infrastructure.
- Send booking confirmations and reminders as required.
- Handle scheduled jobs.
- Implement retry and failure-handling mechanisms.
- Evaluate durable job processing and queue requirements.
- Introduce a separate worker service where appropriate.

**Milestone outcome:** The system can execute scheduled and asynchronous tasks reliably outside the main API request-response cycle.

---

## M9 — Authentication & Authorization

Implement authentication and access control across the application.

**Key deliverables**
- Implement user authentication.
- Secure password handling.
- OAuth2 bearer-token authentication.
- Token creation, validation, and expiration handling.
- Define roles and permissions.
- Protect API endpoints.
- Implement authorization checks.
- Validate access-control behavior through tests.

**Milestone outcome:** The API is secured, and users can access resources according to their permissions.

---

## M10 — Hardening & Production Readiness

Review and improve the complete system before considering it portfolio-ready.

**Key deliverables**
- Review architecture and module boundaries.
- Strengthen validation and error handling.
- Complete meaningful unit, integration, and end-to-end tests.
- Test important business workflows.
- Test concurrency-sensitive operations.
- Review security and configuration practices.
- Improve logging and observability.
- Review database indexes and query performance.
- Prepare deployment configuration.
- Establish CI workflows where appropriate.
- Finalize technical documentation and project README.

**Milestone outcome:** A reliable, maintainable, tested, documented, and demonstrable backend suitable for portfolio presentation.

---

## Optional Future Expansion

The following features are outside the initial core development roadmap and may be introduced later based on actual requirements:

- Learning progress tracking
- Practice logs
- Learning resources and file management
- Advanced student performance analytics
- Payment gateway integration
- Additional automation and reporting features

These features will be evaluated separately rather than included in the initial development scope.

---

## Development Approach

Each milestone will follow an incremental development workflow:

1. Understand the feature and its requirements.
2. Identify entities, attributes, relationships, and constraints.
3. Update the ERD as required.
4. Define implementation tasks and acceptance criteria.
5. Review the technical plan before implementation.
6. Implement in small, manageable slices.
7. Test expected behavior, edge cases, and failure scenarios.
8. Review the implementation and update documentation.
9. Close the milestone before moving forward.

The detailed implementation plan, database design, API specifications, and technical decisions will be developed progressively as each milestone begins.

---

## Guiding Principle

Build the necessary functionality first, maintain engineering quality throughout development, and avoid premature complexity.

StrumSpace should evolve through deliberate, incremental implementation rather than attempting to design and build the entire system upfront.