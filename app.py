import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

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
# Recurrence options
occurrence = st.selectbox("Occurrence", ["once", "daily", "weekly"], index=0)
recurring = st.checkbox("Recurring", value=False)

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
        occurrence=occurrence,
        recurring=recurring,
    )
    current_pet.add_task(task)
    st.success(f"Added task for {current_pet.name}.")

if owner.pets:
    st.write("Current pets and tasks:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.animal_type})")
        if pet.tasks:
            for t_index, task in enumerate(pet.tasks):
                cols = st.columns([6, 1])
                with cols[0]:
                    st.write(
                        f"• {task.type} — {task.importance} ({task.duration_minutes} min)"
                    )
                # Button to mark task completed. Use unique key per task.
                btn_key = f"complete-{pet.name}-{t_index}-{task.type}"
                with cols[1]:
                    if st.button("Complete", key=btn_key):
                            # mark complete and optionally create next occurrence
                            new_task = task.mark_completed()
                            # remove the completed task from the pet
                            pet.remove_task(task)
                            st.success(f"Marked '{task.type}' complete for {pet.name} and removed it.")
                            if new_task is not None:
                                st.info(f"Created next occurrence: {new_task.time}")

                            # if pet has no remaining tasks, remove the pet from owner
                            if not pet.tasks:
                                owner.remove_pet(pet)
                                st.info(f"Removed pet {pet.name} (no remaining tasks).")

                            # regenerate plan if present
                            if "plan" in st.session_state:
                                scheduler = Scheduler(owner=owner, available_slots=["08:00", "09:00", "19:00"])
                                st.session_state.plan = scheduler.generate_schedule(owner.get_all_tasks())
        else:
            st.write("  • No tasks yet")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan from the tasks attached to your pets.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner, available_slots=["08:00", "09:00", "19:00"])

    # Gather tasks and show a sorted preview
    tasks = owner.get_all_tasks()
    if not tasks:
        st.info("No tasks available to schedule yet.")
    else:
        # Detect pre-schedule conflicts based on task.time
        pre_conflict = scheduler.detect_conflicts(tasks)
        if pre_conflict:
            # Build a helpful table of conflicting entries
            dup_times = {}
            for t in tasks:
                dup_times.setdefault(t.time, []).append(t)
            conflict_rows = []
            for tm, items in dup_times.items():
                if len(items) > 1:
                    for it in items:
                        conflict_rows.append({
                            "time": tm,
                            "pet": it.pet.name if it.pet else "Unknown",
                            "task": it.type,
                            "priority": it.importance,
                        })
            st.warning(pre_conflict)
            if conflict_rows:
                st.table(conflict_rows)

        st.markdown("**All tasks (sorted by clock time)**")
        sorted_tasks = scheduler.sort_by_time(tasks)
        preview_rows = [
            {
                "time": t.time,
                "pet": t.pet.name if t.pet else "Unknown",
                "task": t.type,
                "priority": t.importance,
                "duration_min": t.duration_minutes,
            }
            for t in sorted_tasks
        ]
        st.table(preview_rows)

        # Generate the final plan and show results
        plan = scheduler.generate_schedule(tasks)
        st.session_state.plan = plan

        # Check for scheduled-time conflicts (after assignment)
        scheduled_map = {}
        schedule_conflicts = []
        for t in plan:
            key = t.scheduled_time or "UNSCHEDULED"
            scheduled_map.setdefault(key, []).append(t)
        for key, items in scheduled_map.items():
            if key != "UNSCHEDULED" and len(items) > 1:
                schedule_conflicts.append({"scheduled_time": key, "count": len(items)})

        if schedule_conflicts:
            st.warning("Scheduling conflicts detected for these times:")
            st.table(schedule_conflicts)

        if plan:
            st.success("Schedule generated")
            plan_rows = []
            for index, task in enumerate(plan, start=1):
                plan_rows.append(
                    {
                        "#": index,
                        "scheduled_time": task.scheduled_time or "(unscheduled)",
                        "task": task.type,
                        "pet": task.pet.name if task.pet else "Unknown",
                        "priority": task.importance,
                        "duration_min": task.duration_minutes,
                    }
                )
            st.table(plan_rows)
        else:
            st.info("No tasks were scheduled after applying preferences and blockers.")
