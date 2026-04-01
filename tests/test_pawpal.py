import sys
from datetime import date
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Schedule, Task, User


def test_task_completion_changes_status() -> None:
	task = Task(task_type="Feed dinner", priority=3, time_slot="evening")

	assert task.is_completed is False
	task.mark_complete()
	assert task.is_completed is True


def test_complete_daily_task_creates_next_occurrence() -> None:
	owner = User(availability="Mornings")
	pet = Pet(name="Mochi")
	task = Task(
		task_type="Morning walk",
		priority=3,
		time_slot="morning",
		pet=pet,
		recurrence="daily",
		due_date=date(2026, 3, 31),
	)
	owner.schedule_task(task)

	next_task = owner.mark_task_complete(task)

	assert next_task is not None
	assert next_task is not task
	assert next_task.is_completed is False
	assert next_task.task_type == task.task_type
	assert next_task.recurrence == "daily"
	assert next_task.due_date == date(2026, 4, 1)
	assert owner.scheduled_tasks[-1] == next_task


def test_complete_weekly_task_creates_next_occurrence() -> None:
	owner = User(availability="Weeknights")
	pet = Pet(name="Nori")
	task = Task(
		task_type="Brush coat",
		priority=2,
		time_slot="evening",
		pet=pet,
		recurrence="weekly",
		due_date=date(2026, 3, 31),
	)
	owner.schedule_task(task)

	next_task = owner.mark_task_complete(task)

	assert next_task is not None
	assert next_task.recurrence == "weekly"
	assert next_task.pet == pet
	assert next_task.due_date == date(2026, 4, 7)


def test_complete_one_time_task_does_not_create_next_occurrence() -> None:
	owner = User(availability="Evenings")
	task = Task(task_type="Vet reminder", priority=5, time_slot="noon")
	owner.schedule_task(task)

	next_task = owner.mark_task_complete(task)

	assert next_task is None
	assert task.is_completed is True
	assert owner.scheduled_tasks == [task]


def test_recurring_task_requires_due_date() -> None:
	with pytest.raises(ValueError):
		Task(task_type="Daily meds", priority=4, time_slot="morning", recurrence="daily")


def test_schedule_add_task_returns_warning_on_same_pet_same_time_conflict() -> None:
	mochi = Pet(name="Mochi")
	schedule = Schedule(date="2026-03-31")
	first_task = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	second_task = Task(task_type="Feed breakfast", priority=4, time_slot="morning", pet=mochi)

	first_warning = schedule.add_task(first_task)
	conflict_warning = schedule.add_task(second_task)

	assert first_warning is None
	assert conflict_warning is not None
	assert "conflicts" in conflict_warning.lower()
	assert schedule.tasks == [first_task]
	assert schedule.warnings[-1] == conflict_warning


def test_schedule_allows_same_time_for_different_pets() -> None:
	mochi = Pet(name="Mochi")
	nori = Pet(name="Nori")
	schedule = Schedule(date="2026-03-31")
	walk_mochi = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	feed_nori = Task(task_type="Feed breakfast", priority=4, time_slot="morning", pet=nori)

	first_warning = schedule.add_task(walk_mochi)
	second_warning = schedule.add_task(feed_nori)

	assert first_warning is None
	assert second_warning is None
	assert schedule.detect_time_conflicts() == []


def test_schedule_init_collects_warning_when_seeded_with_conflicting_tasks() -> None:
	mochi = Pet(name="Mochi")
	first_task = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	second_task = Task(task_type="Feed breakfast", priority=4, time_slot="morning", pet=mochi)

	schedule = Schedule(date="2026-03-31", tasks=[first_task, second_task])

	assert len(schedule.warnings) == 1
	assert "conflicts" in schedule.warnings[0].lower()


def test_detect_time_conflicts_returns_conflicting_task_pair() -> None:
	mochi = Pet(name="Mochi")
	first_task = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	second_task = Task(task_type="Feed breakfast", priority=4, time_slot="morning", pet=mochi)
	non_conflicting_task = Task(task_type="Evening play", priority=2, time_slot="evening", pet=mochi)

	schedule = Schedule(date="2026-03-31", tasks=[first_task, second_task, non_conflicting_task])
	conflicts = schedule.detect_time_conflicts()

	assert len(conflicts) == 1
	assert conflicts[0] == (first_task, second_task)


def test_adding_task_to_pet_increases_pet_task_count() -> None:
	owner = User(availability="Evenings")
	pet = Pet(name="Mochi")
	owner.add_pet(pet)

	def task_count_for_pet() -> int:
		return sum(1 for task in owner.scheduled_tasks if task.pet == pet)

	before_count = task_count_for_pet()

	task = Task(task_type="Walk", priority=2, time_slot="morning")
	task.assign_to_pet(pet)
	owner.schedule_task(task)

	after_count = task_count_for_pet()
	assert after_count == before_count + 1


def test_filter_tasks_by_completion_status() -> None:
	mochi = Pet(name="Mochi")
	feed_task = Task(task_type="Feed dinner", priority=3, time_slot="evening", pet=mochi)
	walk_task = Task(task_type="Evening walk", priority=2, time_slot="evening", pet=mochi)
	walk_task.mark_complete()

	schedule = Schedule(date="2026-03-31", tasks=[feed_task, walk_task])

	pending_tasks = schedule.filter_tasks(is_completed=False)
	completed_tasks = schedule.filter_tasks(is_completed=True)

	assert pending_tasks == [feed_task]
	assert completed_tasks == [walk_task]


def test_filter_tasks_by_pet_name_case_insensitive() -> None:
	mochi = Pet(name="Mochi")
	nori = Pet(name="Nori")
	feed_mochi = Task(task_type="Feed Mochi", priority=3, time_slot="morning", pet=mochi)
	feed_nori = Task(task_type="Feed Nori", priority=3, time_slot="morning", pet=nori)

	schedule = Schedule(date="2026-03-31", tasks=[feed_mochi, feed_nori])

	mochi_tasks = schedule.filter_tasks(pet_name="  mochi  ")

	assert mochi_tasks == [feed_mochi]


def test_filter_tasks_by_completion_status_and_pet_name() -> None:
	mochi = Pet(name="Mochi")
	nori = Pet(name="Nori")
	mochi_pending = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	mochi_done = Task(task_type="Brush coat", priority=1, time_slot="night", pet=mochi)
	nori_done = Task(task_type="Evening play", priority=2, time_slot="evening", pet=nori)
	mochi_done.mark_complete()
	nori_done.mark_complete()

	schedule = Schedule(date="2026-03-31", tasks=[mochi_pending, mochi_done, nori_done])

	mochi_completed = schedule.filter_tasks(is_completed=True, pet_name="Mochi")

	assert mochi_completed == [mochi_done]


def test_get_daily_plan_sorts_out_of_order_tasks() -> None:
	mochi = Pet(name="Mochi")
	nori = Pet(name="Nori")

	evening_task = Task(task_type="Evening play", priority=2, time_slot="evening", pet=mochi)
	early_feed = Task(task_type="Feed breakfast", priority=5, time_slot="early morning", pet=nori)
	morning_walk = Task(task_type="Morning walk", priority=3, time_slot="morning", pet=mochi)
	completed_noon = Task(task_type="Midday meds", priority=4, time_slot="noon", pet=nori)
	completed_noon.mark_complete()

	schedule = Schedule(date="2026-03-31", tasks=[evening_task, early_feed, morning_walk, completed_noon])

	ordered_tasks = schedule.get_daily_plan()

	assert ordered_tasks == [early_feed, morning_walk, evening_task, completed_noon]


def test_task_setters_validate_and_update_values() -> None:
	task = Task(task_type="Walk", priority=2, time_slot="morning")

	task.set_priority(4)
	task.set_time_slot(" evening ")

	assert task.priority == 4
	assert task.time_slot == "evening"

	with pytest.raises(ValueError):
		task.set_priority(0)

	with pytest.raises(ValueError):
		task.set_time_slot("   ")
