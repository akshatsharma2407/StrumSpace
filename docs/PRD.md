## Product Requirements Document (PRD): StrumSpace

**Document Status:** Production v1.0

**Product Name:** StrumSpace – Guitar Academy Management System

**Target Domain:** In-Person Music Education & Studio Operations

---

### 1. Executive Summary & Problem Statement

Independent music instructors teaching 20 to 50 recurring students rely on fragmented tools—WhatsApp threads, phone calls, paper notebooks, and spreadsheets—to run daily operations. This causes dropped enquiries, double-booked trial sessions, untracked attendance, scattered sheet music, and hours lost to manual reminders.

**StrumSpace** is an end-to-end academy operations platform that centralizes lead capture, trial scheduling, batch organization, student progress, practice materials, and automated communications into a single system of record. The public website and role-based portals serve as clean interfaces over a unified operational core.

---

### 2. Goals & Success Metrics

| Goal | Target Outcome | Key Metric |
| --- | --- | --- |
| **Eliminate Lead Leakage** | Every website visitor enquiry is logged, acknowledged, and tracked to resolution. | 100% automated confirmation delivery; 0 lost enquiries. |
| **Zero Double-Bookings** | Visitors book open trial slots self-serve without instructor coordination or conflicts. | 0 overlapping trial bookings; instant slot release on cancellation. |
| **Centralize Class Operations** | Batches, seat capacities, attendance, and lesson logs live in one place. | Less than 2 minutes required per class to log attendance and lesson notes. |
| **Improve Student Retention** | Students view their learning history, practice materials, and upcoming schedule anytime. | Greater than 85% attendance rate; higher trial-to-batch conversion. |
| **Automate Routine Follow-Ups** | Class reminders and status updates run automatically without manual messaging. | 100% on-time delivery of 24-hour and 1-hour class reminders. |

---

### 3. User Personas & Access Scopes

| Persona | Profile | Core Capabilities |
| --- | --- | --- |
| **Visitor** | Prospective student or parent exploring guitar lessons online. | Browse course offerings, submit class enquiries, view open trial slots, book or cancel a trial class. |
| **Student** | Enrolled learner assigned to an active batch. | Log into personal portal, view batch schedule, review attendance & lesson history, log home practice minutes, download batch-specific practice materials. |
| **Instructor / Admin** | Academy owner/teacher managing daily operations. | Manage enquiry pipeline, publish trial slots, create/edit batches, enroll/remove students, record attendance & lesson progress, upload study materials, trigger/monitor notifications. |

---

### 4. User Experience & Interface Surfaces

1. **Public Academy Landing Page (Visitor View)**
* Clean storefront showcasing course tracks (Acoustic, Electric, Classical), skill levels (Beginner, Intermediate, Advanced), instructor profile, and studio timings.
* Embedded **Class Enquiry Form** and interactive **Trial Slot Picker** displaying real-time available dates and times.


2. **Student Portal (Authenticated View)**
* **Dashboard:** Next upcoming class countdown, overall attendance percentage, total lessons completed, and weekly practice streak.
* **Learning Timeline:** Chronological log of every attended session, topics covered (e.g., *Lesson 02: Open chords – A, D, E*), and instructor feedback.
* **Resource Library:** Downloadable sheet music, chord charts, and audio tracks filtered strictly to the student's enrolled batch.
* **Practice Tracker:** Simple input to log daily home practice minutes.


3. **Instructor Command Center (Admin View)**
* **Lead Pipeline Board:** Filterable list/kanban view of enquiries grouped by status (`NEW` → `CONTACTED` → `TRIAL_BOOKED` → `CONVERTED` / `REJECTED`).
* **Schedule & Batch Manager:** Calendar view of Monday–Saturday trial slots and recurring weekly batches with live seat counts (e.g., *6 / 8 seats filled*).
* **Post-Class Quick Log:** Single-screen roster allowing the instructor to mark attendance, record the lesson summary, and attach practice files immediately after a session.



---

### 5. Functional Requirements

#### 5.1 Smart Class Enquiry & Lead Management

* **Enquiry Capture:** Visitors submit full name, email address, phone number, current skill level (`Beginner`, `Intermediate`, `Advanced`), preferred class timing, preferred guitar type (`Acoustic`, `Electric`, `Classical`), and an optional message.
* **Validation & Deduplication:** Required fields and contact formats are validated upon submission. Repeated submissions from the same contact details within an active window are flagged or merged to prevent duplicate lead clutter.
* **Unique Tracking:** Every valid submission receives a human-readable unique Enquiry ID.
* **Automated Acknowledgement:** Submitting an enquiry immediately sends a confirmation email to the visitor and alerts the instructor.
* **Lifecycle Tracking:** Instructors update lead progression across defined states:
* **Active Path:** `NEW` → `CONTACTED` → `TRIAL_BOOKED` → `CONVERTED`
* **Closed Path:** `NEW` → `CONTACTED` → `REJECTED`



#### 5.2 Trial Class Booking System

* **Slot Publishing:** The instructor defines available Monday–Saturday trial slots with specific dates, start times, and seat capacities (typically 1-on-1).
* **Real-Time Availability:** Visitors see only slots with remaining capacity.
* **Conflict-Free Reservation:** If two visitors attempt to claim the final seat at the exact same moment, only one reservation succeeds; the second visitor is immediately informed the slot is no longer available.
* **Duplicate Booking Prevention:** Accidental double-clicks or repeated submissions for the same visitor and slot produce a single booking rather than duplicate reservations.
* **Cancellation & Instant Release:** Cancelling a booking updates its status to `CANCELLED` and immediately restores the seat to public availability.
* **Booking Lifecycle States:** `PENDING` → `CONFIRMED` → `COMPLETED`, with terminal exceptions for `CANCELLED` and `NO_SHOW`.

#### 5.3 Batch & Class Management

* **Batch Configuration:** Instructors create recurring group batches specifying batch name (e.g., *Beginner A*), skill level, recurring days (e.g., *Mon, Wed*), class time, and maximum seat capacity.
* **Schedule Conflict Guard:** The system prevents creating or rescheduling a batch if the time overlaps with another existing batch or active trial slot for the same instructor.
* **Roster Management:** Instructors add or remove enrolled students from batches.
* **Dynamic Seat Calculation:** Available seats (`Capacity − Enrolled Students`) are calculated automatically in real time whenever students join or leave a batch.

#### 5.4 Attendance & Student Progress Tracking

* **Session Logging:** After each class, the instructor marks each student's attendance (Present / Absent) and logs what was taught (e.g., *Lesson 03: Basic strumming patterns*).
* **Student Learning History:** Students view a complete chronological record of their attended lessons and current skill level.
* **Automated Metrics:** The system automatically calculates and displays:
* Total classes attended and total classes missed
* Overall attendance percentage
* Total lessons completed


* **Home Practice Log:** Students log self-practice sessions (date and minutes practiced) to track consistency between classes.

#### 5.5 Practice Material Management

* **Resource Uploads:** Instructors upload learning materials linked to specific batches or lessons, including:
* Chord charts and lesson handouts (PDF)
* Song sheets and tablature (PDF)
* Practice exercises and study notes (PDF / documents)
* Backing tracks and audio demonstrations (MP3 / WAV)


* **Upload Safeguards:** Only approved file types and reasonable file sizes are accepted; uploaded files are automatically organized by batch and lesson.
* **Access Control:** Practice materials are private to the academy—only instructors and students actively enrolled in the corresponding batch can view or download them.

#### 5.6 Automated Notifications & Reminders

* **Event-Driven Messages:** The system automatically dispatches emails for key lifecycle events:
* Enquiry confirmation (to visitor) and new lead alert (to instructor)
* Trial booking confirmation and cancellation receipt
* Welcome email upon enrollment into a batch


* **Scheduled Class Reminders:** Enrolled students and trial visitors automatically receive:
* A reminder **24 hours** before their scheduled class
* A final reminder **1 hour** before their scheduled class


* **Delivery Reliability:** Notifications are processed reliably in the background so user actions on the website remain instantaneous, with automatic retries and status tracking (`Sent`, `Failed`, `Retry Scheduled`) visible to the admin.

---

### 6. Non-Functional Requirements

* **Responsiveness:** All user-facing actions (submitting forms, booking slots, logging attendance) complete within 1 second without waiting on email delivery.
* **Data Integrity:** Student records, booking histories, attendance logs, and uploaded files persist reliably across system restarts without data loss.
* **Privacy & Role Isolation:** Visitors cannot access student rosters or materials; students can only view their own progress and materials assigned to their batch; only the instructor/admin can modify schedules, statuses, and rosters.
* **Scalability for Studio Growth:** Supports smooth operation for 20–50 active students in Phase 1 while accommodating expansion to 200+ students and multiple instructors without workflow redesign.

---

### 7. Phased Rollout Plan

| Phase | Scope | User Value Delivered |
| --- | --- | --- |
| **Phase 1: Lead & Trial Engine** | Public enquiry form, status tracking, Monday–Saturday trial slot booking, conflict-free reservations, and cancellation handling. | Eliminates manual WhatsApp back-and-forth for new student onboarding. |
| **Phase 2: Automated Communications** | Instant booking/enquiry emails plus automated 24-hour and 1-hour class reminders. | Cuts trial and regular class no-shows without manual texting. |
| **Phase 3: Core Academy Operations** | Batch creation, schedule overlap checks, student enrollment, attendance logging, and lesson progress history. | Replaces paper notebooks and spreadsheets for daily teaching. |
| **Phase 4: Student Portal & Resources** | Student login, practice minute tracker, and batch-restricted uploads/downloads for PDFs and audio lessons. | Gives students a structured home practice hub and increases retention. |

---

### 8. Out of Scope (v1.0)

* Online payment gateway processing and automated recurring invoicing (tracked offline in v1.0).
* Live video conferencing or virtual classroom streaming (academy operates strictly in person).
* Multi-branch franchise management or multi-instructor payroll calculations.