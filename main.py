from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", preferences="keep tasks simple")

    mochi = Pet(name="Mochi", animal_type="dog", health="healthy")
    luna = Pet(name="Luna", animal_type="cat", health="healthy")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    walk = Task(type="Morning Walk", time="09:30", importance="high", duration_minutes=30)
    feed = Task(type="Feeding", time="08:00", importance="high", duration_minutes=10)
    meds = Task(type="Medication", time="08:15", importance="medium", duration_minutes=5)
    groom = Task(type="Grooming", time="10:00", importance="low", duration_minutes=20)
    overlap = Task(type="Overlapping Care", time="08:15", importance="high", duration_minutes=15)

    mochi.add_task(walk)
    mochi.add_task(feed)
    luna.add_task(meds)
    luna.add_task(groom)
    luna.add_task(overlap)

    scheduler = Scheduler(owner=owner, available_slots=["08:00", "09:00", "19:00"])
    all_tasks = owner.get_all_tasks()
    plan = scheduler.build_plan(owner=owner, pet=None)
    if not plan:
        plan = scheduler.generate_schedule(all_tasks)

    sorted_tasks = scheduler.sort_by_time(all_tasks)
    filtered_tasks = scheduler.filter_tasks(all_tasks, completed=False, pet_name="mochi")
    conflict_warning = scheduler.detect_conflicts(all_tasks)

    print("Today's Schedule")
    print("=" * 25)
    for index, task in enumerate(plan, start=1):
        pet_name = task.pet.name if task.pet else "Unknown"
        print(
            f"{index}. {task.scheduled_time} - {task.type} ({pet_name}) | "
            f"Priority: {task.importance} | Duration: {task.duration_minutes} min"
        )

    print("\nSorted by Time")
    print("-" * 20)
    for task in sorted_tasks:
        pet_name = task.pet.name if task.pet else "Unknown"
        print(f"{task.time} - {task.type} ({pet_name})")

    print("\nFiltered for pending Mochi tasks")
    print("-" * 30)
    for task in filtered_tasks:
        print(f"{task.time} - {task.type}")

    if conflict_warning:
        print("\nConflict Warning")
        print("-" * 20)
        print(conflict_warning)


if __name__ == "__main__":
    main()
