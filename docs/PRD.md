# StrumSpace — Product Requirements Document (PRD)

**Document Status:** Phase 0 Baseline  
**Version:** 1.0  
**Last Updated:** 23 November 2026

---

## 1. Product Overview

StrumSpace is a backend-focused Guitar Academy Management System designed to digitize and centralize the day-to-day operations of an offline guitar academy.

The system aims to replace fragmented management practices involving WhatsApp conversations, notebooks, spreadsheets, and manual record-keeping with a structured, reliable, and maintainable application.

StrumSpace will provide APIs to manage prospective students, trial classes, students, batches, attendance, and payment records, while creating a foundation for future operational improvements.

The initial development focus is the backend, its business logic, database design, API behavior, testing, and engineering quality. A frontend is not a priority during the initial development milestones.

---

## 2. Problem Statement

Managing an offline guitar academy through multiple disconnected tools creates operational difficulties, including:

- Enquiry information scattered across messages and records.
- Difficulty tracking prospective students and follow-ups.
- Manual coordination of trial classes and scheduling.
- Lack of centralized student records.
- Difficulty organizing batches and enrollment.
- Inconsistent attendance records.
- Manual tracking of fees and payments.
- Limited visibility into the academy's overall operations.

These practices become increasingly difficult to maintain as the number of students and classes grows.

---

## 3. Product Vision

Build a centralized system that helps a guitar academy manage its operational activities efficiently, maintain reliable records, and provide a foundation for future automation and growth.

StrumSpace is intended to be a realistic, maintainable backend system that demonstrates practical software engineering principles, not merely a collection of CRUD endpoints.

---

## 4. Goals

The primary goals of StrumSpace are:

- Centralize academy operational data.
- Improve enquiry tracking and prospective student management.
- Simplify trial class scheduling and management.
- Maintain structured student records.
- Manage batches and student enrollment.
- Track class attendance.
- Maintain fee and payment records.
- Establish consistent business rules and data integrity.
- Provide reliable, documented APIs.
- Build a maintainable and testable backend architecture.
- Demonstrate practical backend engineering skills through a realistic project.

---

## 5. Core Functional Areas

### 5.1 Enquiry Management

Manage individuals interested in joining the academy.

The system should support:

- Creating enquiries.
- Maintaining prospective student information.
- Retrieving and listing enquiries.
- Updating enquiry details.
- Tracking enquiry status.
- Recording follow-up information.
- Filtering and searching enquiries.
- Managing the transition from enquiry to student where appropriate.

### 5.2 Trial Class Management

Manage trial classes offered to prospective students.

The system should support:

- Trial class scheduling.
- Availability management where required.
- Trial booking and cancellation.
- Booking status tracking.
- Scheduling conflict prevention.
- Associating trial bookings with relevant enquiries.
- Handling booking-related business rules reliably.

### 5.3 Student Management

Maintain centralized student records.

The system should support:

- Creating student records.
- Converting eligible enquiries into student records.
- Retrieving student information.
- Updating student profiles.
- Managing student status and lifecycle.
- Maintaining relevant student history.

### 5.4 Batch Management & Enrollment

Organize students into classes and batches.

The system should support:

- Creating and managing batches.
- Maintaining batch schedules.
- Managing batch capacity.
- Enrolling students.
- Managing enrollment changes.
- Handling scheduling and enrollment constraints.

### 5.5 Attendance Management

Maintain attendance records for academy classes.

The system should support:

- Recording attendance.
- Updating attendance records when corrections are required.
- Retrieving attendance history.
- Student attendance summaries.
- Batch attendance summaries.
- Attendance-related validation and business rules.

### 5.6 Fee & Payment Management

Maintain basic financial records related to student fees and payments.

The system should support:

- Recording fee-related obligations where applicable.
- Recording payments received.
- Maintaining payment dates and amounts.
- Retrieving payment history.
- Tracking outstanding balances where applicable.
- Handling corrections to payment records according to defined rules.

This feature is intended for internal record-keeping. Online payment processing and payment gateway integrations are not part of the initial core scope.

### 5.7 Notifications & Reminders

Support communication and automated reminders for relevant academy activities.

Potential capabilities include:

- Enquiry acknowledgements.
- Trial class booking confirmations.
- Trial class reminders.
- Instructor notifications.
- Scheduled follow-ups.
- Other operational notifications.

The implementation will be introduced when the background processing milestone is reached.

---

## 6. High-Level Operational Workflows

The following workflows represent the intended operational direction of the system. Detailed business rules will be defined during feature development.

### Workflow 1 — Enquiry to Student

1. An individual contacts the academy.
2. Their enquiry is recorded in StrumSpace.
3. The enquiry is tracked and followed up.
4. A trial class may be arranged.
5. The prospective student decides to join.
6. An eligible enquiry is converted into a student record.

### Workflow 2 — Trial Class Booking

1. A prospective student requests a trial class.
2. Appropriate availability is identified.
3. A trial booking is created.
4. The booking is confirmed and tracked.
5. The trial is conducted, cancelled, or otherwise updated according to its status.
6. The outcome may inform the subsequent enquiry or student workflow.

### Workflow 3 — Student Enrollment

1. A student record exists.
2. Suitable batches are identified.
3. The student is enrolled into a batch.
4. Enrollment and batch capacity rules are validated.
5. The student's enrollment is maintained as their academy participation changes.

### Workflow 4 — Class Attendance

1. A batch has a scheduled class.
2. Attendance is recorded for participating students.
3. Attendance records may be corrected when necessary.
4. Attendance history and summaries can be retrieved.

### Workflow 5 — Fee & Payment Record Keeping

1. Fee information is maintained for a student as applicable.
2. Payments are recorded when received.
3. Payment history is maintained.
4. Outstanding balances are calculated where applicable.
5. Financial records can be retrieved for operational reference.

---

## 7. User Categories

The system is intended to support the following user categories over time:

- **Academy Admin:** Manages academy operations, records, batches, enrollment, and payments.
- **Instructor:** Handles assigned classes, students, and attendance-related activities.
- **Student:** May eventually access personal information and learning-related services.
- **Prospective Student:** Participates in enquiry and trial class workflows.

Authentication, roles, permissions, and access restrictions will be implemented in a dedicated development milestone. Detailed permission rules will be defined when that milestone begins.

---

## 8. Non-Functional & Engineering Requirements

StrumSpace should be developed with the following engineering considerations:

### Maintainability
- Clear separation of responsibilities.
- Modular application structure.
- Readable, consistent code.
- Avoid unnecessary coupling.

### Reliability & Data Integrity
- Validate input and business rules.
- Use appropriate database constraints.
- Maintain transaction integrity.
- Handle failures predictably.
- Prevent conflicting operations in concurrency-sensitive workflows.

### Performance
- Use efficient database queries.
- Apply pagination to collection endpoints where appropriate.
- Avoid unnecessary database calls.
- Use asynchronous I/O where beneficial.

### Security
- Secure authentication and authorization.
- Safe handling of credentials and configuration.
- Protect resources from unauthorized access.
- Apply appropriate input validation and security practices.

### Testability
- Unit testing of business logic.
- Integration testing of database interactions.
- API-level and end-to-end testing of important workflows.
- Testing edge cases, failures, and concurrency-sensitive behavior.

### API Consistency
- Versioned REST API.
- Consistent request and response conventions.
- Standardized error handling.
- Predictable resource naming and behavior.

### Timezone Consistency
- The application will use Indian Standard Time (IST), `Asia/Kolkata`, as its operational timezone convention for scheduling and date/time interpretation.

---

## 9. Technical Direction

The project will follow the architectural and technical decisions documented in:

`docs/decisions/ADR-001.md`

The development direction includes:

- Python.
- FastAPI.
- REST APIs.
- MySQL.
- SQLAlchemy 2.x with async support.
- `asyncmy`.
- Alembic for database migrations.
- Pydantic for validation and schemas.
- pytest and supporting testing tools.
- Docker and Docker Compose.

The application will follow a modular monolith architecture. Detailed module structure, entity relationships, API endpoints, and implementation decisions will be developed incrementally during the relevant milestones.

---

## 10. Development Strategy

StrumSpace will be developed incrementally rather than designing the entire system in advance.

Development milestones are maintained separately in:

`docs/DEVELOPMENT-MILESTONES.md`

Each milestone will define the necessary implementation work as it begins, including:

- Requirements and expected behavior.
- Database entities and relationships.
- ERD updates.
- API endpoints and contracts.
- Business logic.
- Validation and constraints.
- Tests.
- Relevant technical decisions.

The database model and ERD will evolve alongside feature development. A complete database schema will not be designed prematurely.

The initial development priority is backend functionality. Frontend implementation may be considered after the backend has matured sufficiently.

---

## 11. Initial Core Scope

The initial core development scope consists of:

1. Backend foundation.
2. Enquiry management.
3. Trial class booking.
4. Student management.
5. Batch and enrollment management.
6. Attendance management.
7. Fee and payment record management.
8. Notifications and background jobs.
9. Authentication and authorization.
10. Hardening, testing, and production readiness.

The detailed sequence and milestone outcomes are maintained in the development milestones document.

---

## 12. Optional Future Expansion

The following are not commitments for the initial core development scope. They may be considered in future iterations:

- Learning progress tracking.
- Practice logs.
- Learning resources and file management.
- Student performance analytics.
- Student-facing portal.
- Instructor-facing portal.
- Frontend application.
- Payment gateway integration.
- Advanced reporting.
- Additional notification and automation workflows.

These features will be evaluated based on actual requirements and the maturity of the core system.

---

## 13. Out of Scope for the Initial Core Development

Unless explicitly introduced in a later decision, the initial core development will not focus on:

- Building a frontend application.
- Online payment processing or payment gateway integration.
- Microservices architecture.
- Designing every future feature and database entity upfront.
- Advanced analytics and reporting.
- Fully automated learning management functionality.
- Overly complex role and permission systems before the authentication milestone.

---

## 14. Success Criteria

StrumSpace will be considered successful as a core backend project when:

- The core academy workflows can be performed through APIs.
- Data is persisted reliably in the database.
- Business rules are consistently enforced.
- Scheduling and enrollment conflicts are handled appropriately.
- Important workflows are covered by meaningful tests.
- Database migrations are managed properly.
- The application follows the agreed architecture and conventions.
- API documentation is clear and usable.
- The project is maintainable and can be extended without major restructuring.
- The developer can confidently explain the architecture, implementation, trade-offs, and engineering decisions.

---

## 15. Guiding Principle

StrumSpace will be built through deliberate, incremental development.

The objective is to build a realistic and maintainable backend that solves the academy's core operational problems while demonstrating sound engineering practices.

The project will prioritize understanding, correctness, and quality over unnecessary complexity or speed of implementation.