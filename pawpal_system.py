from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Owner:
    name: str
    preferences: str = ""
    available_time: str = ""
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's profile."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from the owner's profile."""
        if pet in self.pets:
            self.pets.remove(pet)

    def update_preferences(self, new_preferences: str) -> None:
        """Update the owner's care preferences."""
        self.preferences = new_preferences

    def update_name(self, new_name: str) -> None:
        """Update the owner's name."""
        self.name = new_name


@dataclass
class Pet:
    name: str
    animal_type: str
    health: str = "healthy"
    age: str = ""
    breed: str = ""
    special_needs: str = ""
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Attach a task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task: "Task") -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)
            task.pet = None

    def update_health(self, new_health: str) -> None:
        """Update the pet's health status."""
        self.health = new_health

    def update_profile(self, new_details: dict) -> None:
        """Update pet profile details."""
        for key, value in new_details.items():
            setattr(self, key, value)

    def get_care_needs(self) -> List[str]:
        """Return a list of care needs for the pet."""
        care_needs = [self.health, self.special_needs]
        return [need for need in care_needs if need]


@dataclass
class Task:
    type: str
    time: str
    importance: str = "medium"
    occurrence: str = "once"
    description: str = ""
    duration_minutes: int = 0
    completed: bool = False
    recurring: bool = False
    pet: Optional["Pet"] = None
    scheduled_time: Optional[str] = None
    priority_score: int = 0

    def update_task(self, new_details: dict) -> None:
        """Update task details."""
        for key, value in new_details.items():
            setattr(self, key, value)

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Return whether the task is due today."""
        return self.time.lower() == "today"


class Scheduler:
    def __init__(
        self,
        time: str = "",
        importance: str = "",
        blockers: Optional[List[str]] = None,
        daily_time_limit: int = 0,
        available_slots: Optional[List[str]] = None,
        owner: Optional[Owner] = None,
    ) -> None:
        self.time = time
        self.importance = importance
        self.blockers = blockers or []
        self.daily_time_limit = daily_time_limit
        self.available_slots = available_slots or []
        self.owner = owner
        self.current_plan: List[Task] = []

    def build_plan(self, pet: Pet, tasks: List[Task]) -> List[Task]:
        """Create a plan for a pet based on the available tasks."""
        self.current_plan = self.generate_schedule(tasks)
        return self.current_plan

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by importance or urgency."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks,
            key=lambda task: (
                priority_order.get(task.importance.lower(), 99),
                task.priority_score,
                task.duration_minutes,
            ),
        )

    def resolve_blockers(self, blockers: List[str]) -> List[str]:
        """Handle or remove blockers from the schedule."""
        return [blocker for blocker in blockers if blocker]

    def check_conflicts(self, task: Task, plan: List[Task]) -> bool:
        """Check whether the task conflicts with the existing plan."""
        if not task.scheduled_time:
            return False
        return any(
            existing.scheduled_time == task.scheduled_time
            for existing in plan
            if existing.scheduled_time
        )

    def apply_preferences(self, owner: Owner, tasks: List[Task]) -> List[Task]:
        """Filter or reorder tasks using owner preferences."""
        if not owner.preferences:
            return tasks
        return [task for task in tasks if task.importance.lower() != "low"]

    def generate_schedule(self, tasks: List[Task]) -> List[Task]:
        """Generate a scheduled list of tasks."""
        prioritized = self.prioritize_tasks(tasks)
        resolved_blockers = self.resolve_blockers(self.blockers)
        plan: List[Task] = []
        for task in prioritized:
            if resolved_blockers and task.importance.lower() == "low":
                continue
            if not self.check_conflicts(task, plan):
                plan.append(task)
        return plan

    def explain_plan(self, plan: List[Task]) -> str:
        """Explain why the plan was generated."""
        if not plan:
            return "No plan generated yet."
        task_names = ", ".join(task.type for task in plan)
        return f"Planned tasks: {task_names}"
