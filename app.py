import streamlit as st
from pawpal_system import Pet, Schedule, Task, User


def _initialize_session_state() -> None:
    """Create long-lived session objects once to avoid recreating them on reruns."""
    if st.session_state.get("owner") is None:
        st.session_state.owner = User(availability="Morning and evening")

    if "pets_by_name" not in st.session_state:
        st.session_state.pets_by_name = {}

    if "task_objects" not in st.session_state:
        st.session_state.task_objects = []


_initialize_session_state()

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

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner = st.session_state.owner
    normalized_pet_name = pet_name.strip()

    if not normalized_pet_name:
        st.warning("Enter a pet name before adding a pet.")
    elif normalized_pet_name in st.session_state.pets_by_name:
        st.info(f"{normalized_pet_name} already exists.")
    else:
        new_pet = Pet(name=normalized_pet_name)
        st.session_state.pets_by_name[normalized_pet_name] = new_pet
        owner.add_pet(new_pet)
        st.success(f"Added pet: {normalized_pet_name}")

if st.session_state.pets_by_name:
    st.write("Current pets:")
    st.write(", ".join(st.session_state.pets_by_name.keys()))
else:
    st.info("No pets yet. Add a pet first.")

st.markdown("### Tasks")
st.caption("Schedule tasks by assigning them to an existing pet.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    pet_for_task = st.selectbox(
        "Pet",
        options=list(st.session_state.pets_by_name.keys()) if st.session_state.pets_by_name else [""],
        disabled=not st.session_state.pets_by_name,
    )
with col3:
    time_slot = st.selectbox(
        "Time slot",
        ["early morning", "morning", "noon", "afternoon", "evening", "night"],
        index=1,
    )
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_map = {"low": 1, "medium": 2, "high": 3}
    owner = st.session_state.owner

    if not st.session_state.pets_by_name:
        st.warning("Add at least one pet before scheduling tasks.")
    elif not task_title.strip():
        st.warning("Enter a task title before adding a task.")
    else:
        selected_pet = st.session_state.pets_by_name[pet_for_task]

        new_task = Task(task_type=task_title.strip(), priority=1, time_slot="morning")
        new_task.set_priority(priority_map[priority])
        new_task.set_time_slot(time_slot)
        new_task.assign_to_pet(selected_pet)
        owner.schedule_task(new_task)
        st.session_state.task_objects.append(new_task)
        st.success(f"Added task '{new_task.task_type}' for {selected_pet.name}.")

if st.session_state.task_objects:
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": task.task_type,
                "priority": task.priority,
                "time_slot": task.time_slot,
                "pet": task.pet.name if task.pet else "Unassigned",
            }
            for task in st.session_state.task_objects
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan from your owner's scheduled tasks.")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    owner.set_availability(f"Owner: {owner_name} | Species: {species}")
    schedule = owner.create_daily_schedule(date="Today")
    plan = schedule.get_daily_plan()

    if not plan:
        st.warning("No tasks available to schedule yet.")
    else:
        st.success("Schedule generated.")
        st.table(
            [
                {
                    "time_slot": task.time_slot,
                    "task": task.task_type,
                    "pet": task.pet.name if task.pet else "Unassigned",
                    "priority": task.priority,
                    "completed": task.is_completed,
                }
                for task in plan
            ]
        )
        st.write("Explanation:")
        st.write(schedule.generate_explanation())
