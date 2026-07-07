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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule
=========================
1. 08:00 - Feeding (Mochi) | Priority: high | Duration: 10 min
2. 09:00 - Morning Walk (Mochi) | Priority: high | Duration: 30 min
3. 19:00 - Medication (Luna) | Priority: medium | Duration: 5 min

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
========================================== test session starts ==========================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: *your root dir*
plugins: anyio-4.14.1
collected 14 items     

tests\test_pawpal.py ..............
========================================== 14 passed in 0.16s ==========================================

Confidence Level: 4 Stars
## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sort tasks by clock time (HH:MM). Malformed times are placed last. |
| Prioritization | `Scheduler.prioritize_tasks()` | Sort by `importance` (high→low), then `priority_score`, then `duration_minutes`. |
| Filtering | `Scheduler.filter_tasks()` | Filter by `completed` status and `pet_name`. |
| Conflict detection | `Scheduler.detect_conflicts()`, `Scheduler.check_conflicts()` | `detect_conflicts()` finds duplicate `time` values pre-scheduling; `check_conflicts()` checks `scheduled_time` collisions post-scheduling. |
| Schedule generation | `Scheduler.generate_schedule()` | Assigns tasks to `available_slots`, respects blockers and preferences, and avoids conflicts when possible. |
| Recurrence | `Task.mark_completed()` | Marks completed and creates the next occurrence for `recurring` tasks (`daily`/`weekly`), attaching it to the same `Pet`.
| Preferences & blockers | `Scheduler.apply_preferences()`, `Scheduler.resolve_blockers()` | `apply_preferences()` optionally filters/reorders tasks based on `Owner.preferences`; `resolve_blockers()` cleans or removes blockers. |
| API behavior | `Scheduler.build_plan(owner=None, pet=None)` | Accepts either an `Owner` or a `Pet`; uses `pet.tasks` if `pet` is provided. |
| Explanation | `Scheduler.explain_plan()` | Returns a human-readable summary of the generated plan. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add the owner's name 
2. Add the pet's name and type (dog, cat, or other)
3. Create a task for the pet by giving it a title, duration in minutes, and a priortiy (low, medium, and high). You can create as many tasks as needed for your pet. 
4. If you have more than one pet, add their name and type. Additonally, add the needed tasks for them. To switch between pets to add tasks, simply type their name and type again. 
5. After all tasks are added, click "Generate schedule" to create a schedule. It shows schedules sorted by time and filtered for currently pending pet tasks. It also warns the user
if there's a timing conflict and when. 

Sample CLI Output from running main.py
Today's Schedule
=========================
1. 08:00 - Feeding (Mochi) | Priority: high | Duration: 10 min
2. 09:00 - Overlapping Care (Luna) | Priority: high | Duration: 15 min
3. 19:00 - Morning Walk (Mochi) | Priority: high | Duration: 30 min
4. None - Medication (Luna) | Priority: medium | Duration: 5 min

Sorted by Time
--------------------
08:00 - Feeding (Mochi)
08:15 - Medication (Luna)
08:15 - Overlapping Care (Luna)
09:30 - Morning Walk (Mochi)
10:00 - Grooming (Luna)

Filtered for pending Mochi tasks
------------------------------
09:30 - Morning Walk
08:00 - Feeding

Conflict Warning
--------------------
Warning: overlapping tasks detected at 08:15.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
