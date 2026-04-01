from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pet:
	name: str
	hunger_level: int = 0
	energy_level: int = 0

	def update_hunger(self, level: int) -> None:
		self.hunger_level = max(0, min(10, level))

	def update_energy(self, level: int) -> None:
		self.energy_level = max(0, min(10, level))

	def get_needs_summary(self) -> str:
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

	def assign_to_pet(self, pet: Pet) -> None:
		self.pet = pet

	def set_priority(self, priority: int) -> None:
		if priority < 1:
			raise ValueError("Priority must be at least 1.")
		self.priority = priority

	def set_time_slot(self, time_slot: str) -> None:
		time_slot = time_slot.strip()
		if not time_slot:
			raise ValueError("Time slot cannot be empty.")
		self.time_slot = time_slot

	def mark_complete(self) -> None:
		self.is_completed = True


class Schedule:
	def __init__(self, date: str, tasks: Optional[List[Task]] = None, explanation: str = "") -> None:
		self.date = date
		self.tasks = tasks if tasks is not None else []
		self.explanation = explanation

	def add_task(self, task: Task) -> None:
		self.tasks.append(task)

	def remove_task(self, task: Task) -> None:
		if task in self.tasks:
			self.tasks.remove(task)

	def generate_explanation(self) -> str:
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
		availability = availability.strip()
		if not availability:
			raise ValueError("Availability cannot be empty.")
		self.availability = availability

	def add_pet(self, pet: Pet) -> None:
		self.pets.append(pet)

	def schedule_task(self, task: Task) -> None:
		self.scheduled_tasks.append(task)

	def create_daily_schedule(self, date: str) -> Schedule:
		daily_tasks = [task for task in self.scheduled_tasks if not task.is_completed]
		schedule = Schedule(date=date, tasks=daily_tasks)
		schedule.generate_explanation()
		self.schedules.append(schedule)
		return schedule
