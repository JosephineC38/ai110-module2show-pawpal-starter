from pawpal_system import Owner, Pet, Scheduler, Task
from datetime import date, timedelta


def test_mark_complete_changes_task_status():
    task = Task(type="walk", time="morning", importance="high")

    task.mark_completed()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", animal_type="dog")
    task = Task(type="feed", time="morning", importance="medium")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_by_clock_time():
    scheduler = Scheduler()
    tasks = [
        Task(type="feed", time="09:30", importance="high"),
        Task(type="walk", time="08:00", importance="medium"),
        Task(type="meds", time="08:15", importance="low"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.type for task in sorted_tasks] == ["walk", "meds", "feed"]


def test_daily_recurring_task_creates_next_occurrence_when_completed():
    pet = Pet(name="Mochi", animal_type="dog")
    task = Task(type="feed", time="08:00", importance="high", occurrence="daily", recurring=True)
    pet.add_task(task)

    new_task = task.mark_completed()

    assert task.completed is True
    assert new_task is not None
    assert new_task.completed is False
    assert len(pet.tasks) == 2
    expected_next = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert new_task.time == expected_next


def test_filter_tasks_filters_by_completion_and_pet_name():
    scheduler = Scheduler()
    mochi = Pet(name="Mochi", animal_type="dog")
    luna = Pet(name="Luna", animal_type="cat")
    pending_mochi_task = Task(type="feed", time="08:00", importance="high")
    completed_mochi_task = Task(type="walk", time="09:00", importance="medium")
    completed_luna_task = Task(type="meds", time="10:00", importance="low")

    pending_mochi_task.pet = mochi
    completed_mochi_task.pet = mochi
    completed_luna_task.pet = luna
    completed_mochi_task.completed = True
    completed_luna_task.completed = True

    filtered_tasks = scheduler.filter_tasks(
        [pending_mochi_task, completed_mochi_task, completed_luna_task],
        completed=False,
        pet_name="mochi",
    )

    assert [task.type for task in filtered_tasks] == ["feed"]


def test_detect_conflicts_returns_warning_for_overlapping_tasks():
    scheduler = Scheduler()
    mochi = Pet(name="Mochi", animal_type="dog")
    luna = Pet(name="Luna", animal_type="cat")
    task_one = Task(type="feed", time="08:00", importance="high")
    task_two = Task(type="walk", time="08:00", importance="medium")

    task_one.pet = mochi
    task_two.pet = luna

    warning = scheduler.detect_conflicts([task_one, task_two])

    assert warning == "Warning: overlapping tasks detected at 08:00."


def test_no_tasks_returns_empty_plan():
    owner = Owner(name="Alex")
    scheduler = Scheduler(owner=owner)

    plan = scheduler.build_plan()

    assert plan == []


def test_insufficient_slots_leaves_extras_unscheduled():
    pet = Pet(name="Mochi", animal_type="dog")
    tasks = [
        Task(type="t1", time="08:00", importance="medium"),
        Task(type="t2", time="09:00", importance="medium"),
        Task(type="t3", time="10:00", importance="medium"),
    ]
    for t in tasks:
        pet.add_task(t)

    scheduler = Scheduler(available_slots=["08:00"])
    plan = scheduler.build_plan(pet=pet)

    scheduled = [t for t in plan if t.scheduled_time]
    unscheduled = [t for t in plan if not t.scheduled_time]

    assert len(scheduled) == 1
    assert len(unscheduled) == 2


def test_extra_slots_all_tasks_scheduled():
    pet = Pet(name="Mochi", animal_type="dog")
    tasks = [
        Task(type="a", time="08:00", importance="high"),
        Task(type="b", time="09:00", importance="medium"),
    ]
    for t in tasks:
        pet.add_task(t)

    scheduler = Scheduler(available_slots=["07:00", "08:00", "09:00"])
    plan = scheduler.build_plan(pet=pet)

    assert all(t.scheduled_time for t in plan)


def test_sort_malformed_time_puts_invalid_last():
    scheduler = Scheduler()
    tasks = [
        Task(type="bad", time="bad-time", importance="low"),
        Task(type="ok", time="08:00", importance="low"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [t.type for t in sorted_tasks] == ["ok", "bad"]


def test_prioritize_handles_zero_and_negative_duration():
    scheduler = Scheduler()
    t_neg = Task(type="fast", time="08:00", importance="medium", duration_minutes=-10)
    t_zero = Task(type="short", time="09:00", importance="medium", duration_minutes=0)

    ordered = scheduler.prioritize_tasks([t_zero, t_neg])

    assert [t.duration_minutes for t in ordered] == [-10, 0]


def test_recurring_invalid_occurrence_does_not_create_next():
    pet = Pet(name="Mochi", animal_type="dog")
    task = Task(type="check", time="08:00", recurring=True, occurrence="yearly")
    pet.add_task(task)

    new = task.mark_completed()

    assert new is None
    assert task.completed is True
    assert len(pet.tasks) == 1


def test_recurring_preserves_pet_link():
    pet = Pet(name="Mochi", animal_type="dog")
    task = Task(type="feed", time="08:00", occurrence="daily", recurring=True)
    pet.add_task(task)

    new = task.mark_completed()

    assert new is not None
    assert new.pet is pet


def test_apply_preferences_case_insensitive():
    owner = Owner(name="Sam", preferences="some prefs")
    low = Task(type="low", time="10:00", importance="Low")
    high = Task(type="high", time="11:00", importance="HIGH")
    scheduler = Scheduler()

    filtered = scheduler.apply_preferences(owner, [low, high])

    assert [t.type for t in filtered] == ["high"]
