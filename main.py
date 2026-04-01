from pawpal_system import Pet, Schedule, Task, User


def main() -> None:
	owner = User(availability="Morning and evening")

	pet1 = Pet(name="Mochi", hunger_level=6, energy_level=8)
	pet2 = Pet(name="Nori", hunger_level=8, energy_level=4)

	owner.add_pet(pet1)
	owner.add_pet(pet2)

	# Add tasks in non-chronological order to show schedule sorting.
	task1 = Task(task_type="Evening play", priority=2, time_slot="evening")
	task1.assign_to_pet(pet1)

	task2 = Task(task_type="Feed breakfast", priority=5, time_slot="early morning")
	task2.assign_to_pet(pet2)

	task3 = Task(task_type="Morning walk", priority=3, time_slot="morning")
	task3.assign_to_pet(pet1)

	task4 = Task(task_type="Midday meds", priority=4, time_slot="noon")
	task4.assign_to_pet(pet2)
	task4.mark_complete()

	owner.schedule_task(task1)
	owner.schedule_task(task2)
	owner.schedule_task(task3)
	owner.schedule_task(task4)

	daily_schedule = owner.create_daily_schedule(date="2026-03-31")

	print("PawPal+ Daily Schedule")
	print(f"Owner availability: {owner.availability}")
	print(f"Date: {daily_schedule.date}")
	print("-" * 50)

	for idx, task in enumerate(daily_schedule.get_daily_plan(), start=1):
		pet_name = task.pet.name if task.pet else "Unassigned"
		status = "Done" if task.is_completed else "Pending"
		print(
			f"{idx}. {task.time_slot.title():<14} | "
			f"{task.task_type:<18} | "
			f"Pet: {pet_name:<8} | "
			f"Priority: {task.priority} | "
			f"{status}"
		)

	print("-" * 50)
	print("Pending tasks for Mochi:")
	for task in daily_schedule.filter_tasks(is_completed=False, pet_name="Mochi"):
		print(f"- {task.task_type} ({task.time_slot})")

	print("-" * 50)
	print("Explanation:")
	print(daily_schedule.generate_explanation())


if __name__ == "__main__":
	main()
