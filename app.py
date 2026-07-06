import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Pet and Task Setup")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.update_name(owner_name)

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    matching_pet = next((pet for pet in owner.pets if pet.name == pet_name), None)
    if matching_pet is None:
        new_pet = Pet(name=pet_name, animal_type=species)
        owner.add_pet(new_pet)
        st.success(f"Added pet: {new_pet.name}")
    else:
        st.info(f"{matching_pet.name} is already in your account.")

st.markdown("### Tasks")
st.caption("Create a task for the selected pet and let the scheduler plan it.")

current_pet = next((pet for pet in owner.pets if pet.name == pet_name), None)
if current_pet is None and owner.pets:
    current_pet = owner.pets[0]

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if current_pet is None:
        current_pet = Pet(name=pet_name or "New Pet", animal_type=species)
        owner.add_pet(current_pet)

    task = Task(
        type=task_title,
        time="today",
        importance=priority,
        description=task_title,
        duration_minutes=int(duration),
    )
    current_pet.add_task(task)
    st.success(f"Added task for {current_pet.name}.")

if owner.pets:
    st.write("Current pets and tasks:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.animal_type})")
        if pet.tasks:
            for task in pet.tasks:
                st.write(
                    f"  • {task.type} — {task.importance} ({task.duration_minutes} min)"
                )
        else:
            st.write("  • No tasks yet")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan from the tasks attached to your pets.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner, available_slots=["08:00", "09:00", "19:00"])
    plan = scheduler.build_plan(owner=owner)
    st.session_state.plan = plan
    st.write(scheduler.explain_plan(plan))

    if plan:
        st.write("### Planned Tasks")
        for index, task in enumerate(plan, start=1):
            pet_name_for_task = task.pet.name if task.pet else "Unknown"
            st.write(
                f"{index}. {task.scheduled_time} - {task.type} ({pet_name_for_task}) | "
                f"Priority: {task.importance} | Duration: {task.duration_minutes} min"
            )
    else:
        st.info("No tasks available to schedule yet.")
