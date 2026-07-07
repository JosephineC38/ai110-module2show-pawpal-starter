from pawpal_system import Pet, Scheduler, Task


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
