# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling
Here’s a summary of the new features now in your PawPal scheduler:

1. Recurring task support
- Tasks now support recurrence values: `none`, `daily`, and `weekly`.
- Validation happens at creation time so invalid recurrence values are rejected.
- Implemented in pawpal_system.py.

2. Due dates for recurring tasks
- `daily` and `weekly` tasks require a `due_date`.
- Marking a recurring task complete creates a new task instance with the next due date calculated using `timedelta`:
- Daily: +1 day
- Weekly: +7 days
- Implemented in pawpal_system.py.

3. Completion workflow helper
- Added `mark_task_complete` on `User` as a wrapper around completion logic.
- It marks the current task complete and auto-schedules the next recurring instance (when applicable).
- Implemented in pawpal_system.py.

4. Time conflict detection in Schedule
- Schedule now detects same-pet, same-time conflicts.
- Conflict utilities include checking one candidate and scanning all conflicts.
- Implemented in pawpal_system.py.

5. Lightweight conflict handling (non-crashing)
- Conflict handling was changed from raising errors to returning warning messages.
- `Schedule` now stores warnings in `self.warnings` so the app can continue running.
- Implemented in pawpal_system.py.

6. Improved task filtering
- `filter_tasks` was refactored into a cleaner one-pass implementation.
- Supports filtering by completion status and/or pet name with normalized matching.
- Implemented in pawpal_system.py.

7. Expanded automated tests
- Added tests for:
- recurring task rollover (`daily` and `weekly`)
- due-date requirement validation
- conflict detection and warning behavior
- direct conflict-pair detection
- filtering and sorting behavior
- Test coverage is in test_pawpal.py.

## Testing PawPal+ 

Run the automated tests with:

```bash
python -m pytest
```

Current tests cover the core scheduling behaviors, including recurring task rollover (`daily` and `weekly`), due-date validation, task completion flow, sorting correctness, filtering by completion/pet, and same-pet/same-time conflict detection (including conflict warnings and pair detection).

Confidence in system reliability: **5/5** based on the latest test run with all tests passing.

## Mermaid.js diagram
classDiagram
    class User {
        -preferences: String
        -availability: String
        -pets: List~Pet~
        -scheduledTasks: List~Task~
        +setPreferences(preferences: String) void
        +setAvailability(availability: String) void
        +addPet(pet: Pet) void
        +scheduleTask(task: Task) void
        +createDailySchedule(date: String) Schedule
    }

    class Pet {
        -name: String
        -traits: List~String~
        -hungerLevel: int
        -energyLevel: int
        +setTraits(traits: List~String~) void
        +updateHunger(level: int) void
        +updateEnergy(level: int) void
        +getNeedsSummary() String
    }

    class Task {
        -taskType: String
        -priority: int
        -timeSlot: String
        -notes: String
        +assignToPet(pet: Pet) void
        +setPriority(priority: int) void
        +setTimeSlot(timeSlot: String) void
        +markComplete() void
    }

    class Schedule {
        -date: String
        -tasks: List~Task~
        -explanation: String
        +addTask(task: Task) void
        +removeTask(task: Task) void
        +generateExplanation() String
        +getDailyPlan() List~Task~
    }

    User "1" o-- "*" Pet : owns
    User "1" --> "*" Task : schedules
    User "1" --> "*" Schedule : creates
    Schedule "1" *-- "*" Task : contains
    Pet "1" --> "*" Task : needs