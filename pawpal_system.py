from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Tuple


@dataclass
class Pet:
	name: str
	hunger_level: int = 0
	energy_level: int = 0

	def update_hunger(self, level: int) -> None:
		"""Update hunger level while keeping it within the 0-10 range."""
		self.hunger_level = max(0, min(10, level))

	def update_energy(self, level: int) -> None:
		"""Update energy level while keeping it within the 0-10 range."""
		self.energy_level = max(0, min(10, level))

	def get_needs_summary(self) -> str:
		"""Return a short summary of the pet's current hunger and energy needs."""
		hunger_status = "high" if self.hunger_level >= 7 else "moderate" if self.hunger_level >= 4 else "low"
		energy_status = "low" if self.energy_level <= 3 else "moderate" if self.energy_level <= 6 else "high"
		return (
			f"{self.name}: hunger is {hunger_status} ({self.hunger_level}/10), "
			f"energy is {energy_status} ({self.energy_level}/10)."
		)


@dataclass
class Task:
	task_type: str
	priority: int
	time_slot: str
	pet: Optional[Pet] = None
	is_completed: bool = False
	recurrence: str = "none"
	due_date: Optional[date] = None

	def __post_init__(self) -> None:
		"""Validate recurrence and due date values at task creation time."""
		allowed_recurrence = {"none", "daily", "weekly"}
		normalized_recurrence = self.recurrence.strip().lower()
		if normalized_recurrence not in allowed_recurrence:
			raise ValueError("Recurrence must be 'none', 'daily', or 'weekly'.")
		if normalized_recurrence in {"daily", "weekly"} and self.due_date is None:
			raise ValueError("Daily and weekly tasks must include a due date.")
		self.recurrence = normalized_recurrence

	def assign_to_pet(self, pet: Pet) -> None:
		"""Assign this task to a specific pet."""
		self.pet = pet

	def set_priority(self, priority: int) -> None:
		"""Set task priority, requiring a minimum value of 1."""
		if priority < 1:
			raise ValueError("Priority must be at least 1.")
		self.priority = priority

	def set_time_slot(self, time_slot: str) -> None:
		"""Set the task time slot after validating it is not blank."""
		time_slot = time_slot.strip()
		if not time_slot:
			raise ValueError("Time slot cannot be empty.")
		self.time_slot = time_slot

	def mark_complete(self) -> Optional["Task"]:
		"""Mark this task complete and create the next recurring occurrence if needed."""
		self.is_completed = True

		if self.recurrence in {"daily", "weekly"}:
			if self.due_date is None:
				raise ValueError("Recurring task is missing a due date.")

			days_until_next_due = 1 if self.recurrence == "daily" else 7
			next_due_date = self.due_date + timedelta(days=days_until_next_due)

			return Task(
				task_type=self.task_type,
				priority=self.priority,
				time_slot=self.time_slot,
				pet=self.pet,
				recurrence=self.recurrence,
				due_date=next_due_date,
			)

		return None


class Schedule:
	def __init__(self, date: str, tasks: Optional[List[Task]] = None, explanation: str = "") -> None:
		self.date = date
		self.tasks = tasks if tasks is not None else []
		self.explanation = explanation
		self.warnings: List[str] = []
		for task, other_task in self.detect_time_conflicts():
			self.warnings.append(self._build_conflict_message(task, other_task))

	def add_task(self, task: Task) -> Optional[str]:
		"""Add a task to this schedule, returning a warning message on conflict."""
		if self.has_time_conflict(task):
			conflicting_task = next(
				existing_task
				for existing_task in self.tasks
				if existing_task.pet is not None
				and task.pet is not None
				and existing_task.pet.name.strip().lower() == task.pet.name.strip().lower()
				and existing_task.time_slot.strip().lower() == task.time_slot.strip().lower()
			)
			warning = self._build_conflict_message(task, conflicting_task)
			self.warnings.append(warning)
			return warning
		self.tasks.append(task)
		return None

	def _build_conflict_message(self, task: Task, other_task: Task) -> str:
		"""Build a plain warning for a same-pet same-time conflict."""
		pet_name = task.pet.name if task.pet is not None else "Unassigned pet"
		time_slot = task.time_slot.strip().lower()
		return (
			f"Warning: '{task.task_type}' conflicts with '{other_task.task_type}' "
			f"for {pet_name} at {time_slot}."
		)

	def has_time_conflict(self, candidate_task: Task) -> bool:
		"""Return True when candidate task overlaps with an existing task for the same pet and slot."""
		if candidate_task.pet is None:
			return False

		candidate_pet_name = candidate_task.pet.name.strip().lower()
		candidate_time_slot = candidate_task.time_slot.strip().lower()

		for existing_task in self.tasks:
			if existing_task is candidate_task or existing_task.pet is None:
				continue

			same_pet = existing_task.pet.name.strip().lower() == candidate_pet_name
			same_time_slot = existing_task.time_slot.strip().lower() == candidate_time_slot
			if same_pet and same_time_slot:
				return True

		return False

	def detect_time_conflicts(self) -> List[Tuple[Task, Task]]:
		"""Return all task pairs that conflict by pet and time slot."""
		conflicts: List[Tuple[Task, Task]] = []
		for idx, task in enumerate(self.tasks):
			if task.pet is None:
				continue

			for other_task in self.tasks[idx + 1 :]:
				if other_task.pet is None:
					continue

				same_pet = task.pet.name.strip().lower() == other_task.pet.name.strip().lower()
				same_time_slot = task.time_slot.strip().lower() == other_task.time_slot.strip().lower()
				if same_pet and same_time_slot:
					conflicts.append((task, other_task))

		return conflicts

	def remove_task(self, task: Task) -> None:
		"""Remove a task from this schedule if it exists."""
		if task in self.tasks:
			self.tasks.remove(task)

	def generate_explanation(self) -> str:
		"""Generate and return a plain-language explanation of the schedule."""
		if not self.tasks:
			self.explanation = "No tasks were scheduled for this day."
			return self.explanation

		ordered_tasks = self.get_daily_plan()
		reasons: List[str] = []
		for task in ordered_tasks:
			pet_name = task.pet.name if task.pet else "your pet"
			reasons.append(
				f"{task.task_type} for {pet_name} at {task.time_slot} (priority {task.priority})"
			)

		self.explanation = "Schedule prioritized by urgency, then organized by time slot: " + "; ".join(reasons) + "."
		return self.explanation

	def get_daily_plan(self) -> List[Task]:
		"""Return tasks sorted by completion state, priority, and time slot."""
		time_order = {
			"early morning": 0,
			"morning": 1,
			"noon": 2,
			"afternoon": 3,
			"evening": 4,
			"night": 5,
		}

		return sorted(
			self.tasks,
			key=lambda task: (
				task.is_completed,
				-task.priority,
				time_order.get(task.time_slot.lower(), 99),
				task.time_slot.lower(),
				task.task_type.lower(),
			),
		)

	def filter_tasks(self, is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
		"""Return tasks filtered by completion status and/or pet name."""
		normalized_pet_name: Optional[str] = None
		if pet_name is not None:
			normalized_pet_name = pet_name.strip().lower()
			if not normalized_pet_name:
				raise ValueError("Pet name cannot be empty.")

		return [
			task
			for task in self.tasks
			if (is_completed is None or task.is_completed == is_completed)
			and (
				normalized_pet_name is None
				or (task.pet is not None and task.pet.name.strip().lower() == normalized_pet_name)
			)
		]


class User:
	def __init__(
		self,
		availability: str,
		pets: Optional[List[Pet]] = None,
		scheduled_tasks: Optional[List[Task]] = None,
		schedules: Optional[List[Schedule]] = None,
	) -> None:
		self.availability = availability
		self.pets = pets if pets is not None else []
		self.scheduled_tasks = scheduled_tasks if scheduled_tasks is not None else []
		self.schedules = schedules if schedules is not None else []

	def set_availability(self, availability: str) -> None:
		"""Update owner availability after validating non-empty input."""
		availability = availability.strip()
		if not availability:
			raise ValueError("Availability cannot be empty.")
		self.availability = availability

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this user's pet list."""
		self.pets.append(pet)

	def schedule_task(self, task: Task) -> None:
		"""Add a task to this user's scheduled task list."""
		self.scheduled_tasks.append(task)

	def complete_task(self, task: Task) -> Optional[Task]:
		"""Mark a task complete and auto-schedule its next occurrence when recurring."""
		next_task = task.mark_complete()
		if next_task is not None:
			self.schedule_task(next_task)
		return next_task

	def mark_task_complete(self, task: Task) -> Optional[Task]:
		"""Compatibility wrapper for task completion with recurrence support."""
		return self.complete_task(task)

	def create_daily_schedule(self, date: str) -> Schedule:
		"""Create and store a daily schedule from incomplete scheduled tasks."""
		daily_tasks = [task for task in self.scheduled_tasks if not task.is_completed]
		schedule = Schedule(date=date, tasks=daily_tasks)
		schedule.generate_explanation()
		self.schedules.append(schedule)
		return schedule
