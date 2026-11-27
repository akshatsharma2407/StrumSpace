# StrumSpace — Enquiry Domain & Business Rules

**Phase:** 2 — Enquiry Management (M2)  
**Task:** 2.1 — Enquiry Domain Discovery and Business Rules  
**Status:** Agreed business requirements — ready for Task 2.2

---

## 1. Purpose and Scope

An enquiry represents a prospective student's interest in joining the guitar academy. Enquiries originate from the enquiry form on the StrumSpace website and are maintained centrally for the internal academy team.

This module supports enquiry creation, retrieval, updates, status tracking, basic follow-up management, and repeated enquiries. It does not attempt to provide a complete CRM system.

The current academy has no dedicated staff. The internal team refers to the academy owner and other authorized internal members.

Manual registration of enquiries received through WhatsApp, phone calls, Instagram, referrals, or walk-in visits is not required for M2. Frontend design and implementation are outside the scope of this document.

---

## 2. Enquiry Information

The following table defines the logical information required by the enquiry workflow. Physical database column definitions, data types, indexes, and constraints will be finalized in Task 2.2.

| Field | Required | Managed by | Description |
|---|---|---|---|
| `id` | System-generated | System | Unique identifier for each enquiry. |
| `full_name` | Yes | Visitor / internal team | Name of the prospective student. |
| `phone_number` | Yes | Visitor / internal team | Indian mobile number used for contact and repeated-enquiry lookup. |
| `email` | No | Visitor / internal team | Alternative contact information. |
| `age` | No | Visitor / internal team | Age of the prospective student. |
| `experience_level` | No | Visitor / internal team | Current guitar-playing experience. |
| `message` | No | Visitor / internal team | Additional information or requirements supplied by the visitor. |
| `status` | System-initialized | Internal team | Current enquiry status; defaults to `NEW`. |
| `last_contacted_at` | No | Internal team | Date and time of the most recent contact. |
| `next_follow_up_at` | No | Internal team | Planned date and time of the next follow-up. |
| `created_at` | System-generated | System | Date and time when the enquiry was created. |
| `updated_at` | System-generated | System | Date and time when the enquiry was last modified. |

The module must not include `source` or internal `notes` fields. Additional personal information must not be collected without an approved requirement.

---

## 3. Enquiry Status and Lifecycle

### 3.1 Supported statuses

| Status | Meaning |
|---|---|
| `NEW` | The enquiry has been received but has not yet been contacted. |
| `CONTACTED` | The academy has contacted the prospective student. |
| `INTERESTED` | The prospective student has expressed interest in joining. |
| `NOT_INTERESTED` | The prospective student has indicated that they are not interested. |
| `CLOSED` | The enquiry is no longer being actively pursued. |

### 3.2 Status rules

- Every new enquiry starts with `NEW`. Visitors cannot supply or override the initial status.
- The internal team may change an enquiry from any valid status to any other valid status, including reopening a `CLOSED` enquiry.
- No restrictive status-transition matrix or state machine is required.
- Assigning the existing status again is permitted and does not constitute a new transition.
- Unsupported status values must be rejected.
- Visitors may view the status of their own enquiries but cannot change it.
- Ordinary edits to enquiry information do not automatically change the status.
- `CLOSED` is not an irreversible terminal status for the internal team, but a visitor cannot edit an enquiry while it is closed.
- Trial-booking and student-conversion statuses or workflows are deferred to their respective milestones.

---

## 4. Repeated and Duplicate Enquiries

A repeated enquiry occurs when a visitor submits or attempts to submit enquiry information using a phone number already associated with one or more existing enquiries.

### 4.1 Lookup and handling policy

- Normalize the phone number before checking for existing enquiries.
- If no matching enquiry exists, allow creation of a new enquiry.
- If matching enquiries exist, the intended workflow allows the verified visitor to access their existing enquiries and choose whether to edit an eligible enquiry or create a separate enquiry.
- If an existing enquiry is `CLOSED`, the visitor cannot update it and must create a new enquiry instead, unless the internal team independently reopens the existing record.
- A repeated phone number is not, by itself, a reason to reject a deliberately submitted new enquiry.
- Do not automatically overwrite, merge, delete, or reopen existing enquiries when another enquiry is submitted.

### 4.2 Record independence

- Phone numbers must not be globally unique across enquiry records.
- Each enquiry has its own unique identifier, status, follow-up information, and timestamps.
- Multiple enquiries may share a phone number, including enquiries for different prospective students.
- No separate parent/guardian or household entity is required for M2.
- Creating a new enquiry is distinct from reopening an existing enquiry. A new enquiry begins with `NEW`; previous records remain unchanged.

The exact API contract for lookup and explicit new-enquiry submission will be defined in Task 2.3. Accidental duplicate submissions caused by retries or repeated requests are a separate technical concern from intentionally creating another enquiry; the handling mechanism, if required, will be reviewed during implementation rather than imposing phone-number uniqueness.

---

## 5. Enquiry Update Rules

### 5.1 Visitor updates

A visitor may update the visitor-managed fields of their own enquiry, provided the enquiry is not closed and the visitor's access has been verified.

| Current status | Visitor may edit enquiry information |
|---|---|
| `NEW` | Yes |
| `CONTACTED` | Yes |
| `INTERESTED` | Yes |
| `NOT_INTERESTED` | Yes |
| `CLOSED` | No |

A visitor cannot update the status, follow-up information, identifier, or system-generated timestamps.

### 5.2 Internal team updates

The internal team may update enquiry information, status, and follow-up information regardless of the enquiry's current status. The identifier and system-generated timestamps remain system-managed.

### 5.3 Partial updates

- Only explicitly supplied fields should be updated.
- Omitted fields must retain their existing values.
- Required fields cannot be cleared or set to null.
- Optional fields may be cleared where permitted by the API contract.
- Updates must satisfy the same applicable validation rules as creation.
- A successful update must maintain the system-managed modification timestamp.

Neither visitors nor internal members are permitted to delete enquiry records in M2.

---

## 6. Follow-up Management

Follow-up management is intentionally limited to two optional fields on an enquiry:

- `last_contacted_at`: when the internal team last contacted the prospective student.
- `next_follow_up_at`: when the internal team intends to contact the prospective student again.

Both fields are maintained by the internal team. The internal team can use follow-up date filters to identify upcoming or overdue follow-ups.

No separate follow-up entity, communication history, internal notes, automatic reminders, or scheduling subsystem is required in M2. Status changes do not implicitly update follow-up fields unless such behavior is explicitly approved later.

---

## 7. Validation Rules

### 7.1 Full name

- Required and must not be empty or contain only whitespace.
- Trim surrounding whitespace.
- Do not impose unnecessary restrictions on valid names.

### 7.2 Phone number

- Required; only Indian mobile numbers are supported.
- Accept a valid 10-digit Indian mobile number, optionally prefixed with `+91`, and normalize supported formatting such as spaces.
- Validate that the 10-digit national mobile number starts with a digit from 6 to 9.
- Store the canonical value in `+91XXXXXXXXXX` format.
- Reject invalid mobile numbers and non-Indian numbers.
- Format validation does not establish ownership of the number.

### 7.3 Email

- Optional.
- Must have a valid email format when supplied.
- Email is not required to be unique across enquiries.

### 7.4 Age

- Optional.
- Must be a positive integer when supplied.
- No additional age eligibility restriction has been agreed for M2.

### 7.5 Experience level

Optional, with the following accepted values:

- `BEGINNER`
- `INTERMEDIATE`
- `ADVANCED`

Reject unsupported values when the field is supplied.

### 7.6 Message

- Optional free-text information from the visitor.
- Length limits will be defined during the data-model and API-contract tasks.

### 7.7 Timestamps and data integrity

- All date/time handling must follow the IST (`Asia/Kolkata`) convention established in ADR-001.
- Identifiers and creation/modification timestamps must be system-managed.
- Related database writes must be atomic whenever an operation requires multiple changes: either all changes succeed or the entire operation is rolled back.
- Use the existing Phase 1 session management, transaction strategy, and standardized error handling.

---

## 8. Intended Access and Security Boundaries

The following matrix describes intended business permissions, not the authentication implementation for this phase.

| Operation | Visitor | Internal team |
|---|---|---|
| Create enquiry | Yes | Not required in M2 |
| View own enquiries and their statuses | Yes, after verification | Yes |
| View all enquiries | No | Yes |
| Edit visitor-managed enquiry fields | Own non-closed enquiries only | Yes, including closed enquiries |
| Change enquiry status | No | Yes |
| Manage follow-up information | No | Yes |
| Search, filter, sort, and paginate all enquiries | No | Yes |
| Delete enquiry | No | No |

### Security requirements

- A phone number or enquiry identifier alone must never be treated as proof of ownership.
- Do not reveal existing enquiry records or whether a phone number has submitted enquiries to an unverified public requester.
- Visitor-facing responses must not expose internal follow-up information; the visitor may see their own submitted information and status.
- Authentication, ownership verification, and authorization enforcement remain deferred to M9. The precise verification mechanism (such as OTP or authenticated identity) has not been selected.
- Until these protections are implemented, enquiry APIs must remain restricted to local development/testing with synthetic data. Do not expose unauthenticated retrieval, listing, or update endpoints publicly.
- Any development-only simulation of visitor or internal access must not be presented as production-ready authorization.

---

## 9. Search, Filtering, Sorting, and Pagination

The internal team should be able to retrieve and manage enquiries efficiently through the collection API.

| Capability | Supported fields or behavior |
|---|---|
| Search | Full name, phone number, email |
| Filtering | Status, experience level |
| Date filtering | Creation date and next follow-up date |
| Sorting | Creation time, modification time, next follow-up time |
| Default ordering | Newest enquiries first |
| Pagination | `limit` and `offset`, following ADR-001 |
| Total count | Exact count of records matching the applied search and filters, before pagination |

Ordering must be deterministic when multiple records have the same sort value. Closed enquiries remain available to the internal team and can be retrieved using the supported status filter.

Exact query parameter names, date-range semantics, search matching behavior, null ordering, and pagination limits will be finalized during Task 2.3 in accordance with ADR-001.

No advanced search engine, analytics, or reporting infrastructure is required.

---

## 10. Supported Operations and Scope Boundaries

M2 includes enquiry creation, retrieval, listing, partial updates, status changes, reopening by the internal team, basic follow-up updates, and handling repeated enquiries.

The following are outside the current scope:

- Permanent deletion and soft deletion.
- Manual entry of enquiries from external communication channels.
- Source tracking and internal notes.
- Separate follow-up history or CRM features.
- Trial-class booking and availability (M3).
- Student creation and enquiry-to-student conversion (M4).
- Notifications and automated reminders (M8).
- Authentication and authorization implementation (M9).
- Frontend implementation and form/dropdown design.
- Docker and production deployment infrastructure.

---

## 11. Handoff to Task 2.2

The approved business rules in this document are the basis for the enquiry data model and ERD.

During Task 2.2, define the minimum database structure required to support these rules, including column names and types, nullability, defaults, constraints, indexes, status representation, and timestamp handling. In particular, support normalized phone-number lookup without imposing uniqueness on the phone number.

Use the existing MySQL 8.4, asynchronous SQLAlchemy, Alembic, and isolated test database foundation. Do not create speculative entities for future milestones.

During Task 2.3, define the API schemas, lookup and submission contracts, visitor-managed and internal-team-managed fields, error behavior, and collection query parameters. Any unresolved implementation detail must be reviewed before it becomes a new business rule.

This document does not authorize implementation of subsequent tasks without the project owner's approval.
