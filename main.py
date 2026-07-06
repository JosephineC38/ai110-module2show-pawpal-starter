from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", preferences="keep tasks simple")

    mochi = Pet(name="Mochi", animal_type="dog", health="healthy")
    luna = Pet(name="Luna", animal_type="cat", health="healthy")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    walk = Task(type="Morning Walk", time="today", importance="high", duration_minutes=30)
    feed = Task(type="Feeding", time="today", importance="high", duration_minutes=10)
    meds = Task(type="Medication", time="today", importance="medium", duration_minutes=5)

    mochi.add_task(walk)
    mochi.add_task(feed)
    luna.add_task(meds)

    scheduler = Scheduler(owner=owner, available_slots=["08:00", "09:00", "19:00"])
    all_tasks = owner.get_all_tasks()
    plan = scheduler.build_plan(owner=owner, pet=None)
    if not plan:
        plan = scheduler.generate_schedule(all_tasks)

    print("Today's Schedule")
    print("=" * 25)
    for index, task in enumerate(plan, start=1):
        pet_name = task.pet.name if task.pet else "Unknown"
        print(
            f"{index}. {task.scheduled_time} - {task.type} ({pet_name}) | "
            f"Priority: {task.importance} | Duration: {task.duration_minutes} min"
        )


if __name__ == "__main__":
    main()
