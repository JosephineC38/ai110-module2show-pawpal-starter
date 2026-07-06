from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task(type="walk", time="morning", importance="high")

    task.mark_completed()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", animal_type="dog")
    task = Task(type="feed", time="morning", importance="medium")

    pet.add_task(task)

    assert len(pet.tasks) == 1
