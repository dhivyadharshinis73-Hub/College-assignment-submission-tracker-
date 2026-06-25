from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from .models import Assignment, SubmissionStatus
from .storage import AssignmentStorage


class AssignmentTrackerApp:
    DATA_FILE = Path("data") / "assignments.json"

    def __init__(self) -> None:
        self.storage = AssignmentStorage(self.DATA_FILE)
        self.assignments: List[Assignment] = self.storage.load()

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self._add_assignment()
            elif choice == "2":
                self._update_status()
            elif choice == "3":
                self._list_assignments()
            elif choice == "4":
                self._dashboard_summary()
            elif choice == "5":
                self._filter_by_subject()
            elif choice == "6":
                self._exit()
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

    def _print_menu(self) -> None:
        print("\nCollege Assignment Submission Tracker")
        print("1. Add assignment")
        print("2. Update submission status")
        print("3. List assignments")
        print("4. Dashboard summary")
        print("5. Filter by subject")
        print("6. Exit")

    def _add_assignment(self) -> None:
        title = input("Assignment title: ").strip()
        subject = input("Subject: ").strip()
        due_date = self._prompt_due_date()
        assignment = Assignment(title=title, subject=subject, due_date=due_date)
        self.assignments.append(assignment)
        self.storage.save(self.assignments)
        print(f"Added assignment '{title}' for {subject} due on {due_date.isoformat()}.")

    def _prompt_due_date(self) -> date:
        while True:
            raw = input("Due date (YYYY-MM-DD): ").strip()
            try:
                due_date = datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                continue
            return due_date

    def _update_status(self) -> None:
        if not self.assignments:
            print("No assignments available.")
            return

        self._print_assignments(self.assignments)
        index = self._prompt_index(len(self.assignments))
        assignment = self.assignments[index]
        status = self._prompt_status()
        assignment.status = status
        self.storage.save(self.assignments)
        print(f"Updated assignment '{assignment.title}' status to {assignment.status.value}.")

    def _prompt_index(self, count: int) -> int:
        while True:
            raw = input(f"Enter assignment number (1-{count}): ").strip()
            if raw.isdigit():
                index = int(raw) - 1
                if 0 <= index < count:
                    return index
            print("Invalid assignment number.")

    def _prompt_status(self) -> SubmissionStatus:
        print("Submission status options:")
        for i, status in enumerate(SubmissionStatus, start=1):
            print(f"{i}. {status.value}")
        while True:
            raw = input("Choose status: ").strip()
            if raw.isdigit():
                index = int(raw) - 1
                if 0 <= index < len(SubmissionStatus):
                    return list(SubmissionStatus)[index]
            print("Invalid status selection.")

    def _list_assignments(self) -> None:
        if not self.assignments:
            print("No assignments available.")
            return
        self._print_assignments(self.assignments)

    def _dashboard_summary(self) -> None:
        summary = self._compute_summary(self.assignments)
        print("\nDashboard summary:")
        print(f"Total assignments: {summary['total']}")
        print(f"Submitted: {summary['submitted']}")
        print(f"Pending: {summary['pending']}")
        print(f"Late: {summary['late']}")

    def _filter_by_subject(self) -> None:
        subject = input("Subject to filter by: ").strip()
        filtered = [assignment for assignment in self.assignments if assignment.subject.lower() == subject.lower()]
        if not filtered:
            print(f"No assignments found for subject '{subject}'.")
            return
        self._print_assignments(filtered)

    def _exit(self) -> None:
        print("Exiting Assignment Submission Tracker. Goodbye!")

    def _print_assignments(self, assignments: List[Assignment]) -> None:
        print("\nAssignments:")
        for idx, assignment in enumerate(assignments, start=1):
            print(
                f"{idx}. {assignment.title} | Subject: {assignment.subject} | Due: {assignment.due_date.isoformat()} | Status: {assignment.status.value}"
            )

    @staticmethod
    def _compute_summary(assignments: List[Assignment]) -> dict:
        counts = {"submitted": 0, "pending": 0, "late": 0}
        for assignment in assignments:
            if assignment.status == SubmissionStatus.SUBMITTED:
                counts["submitted"] += 1
            elif assignment.status == SubmissionStatus.PENDING:
                counts["pending"] += 1
            elif assignment.status == SubmissionStatus.LATE:
                counts["late"] += 1
        counts["total"] = len(assignments)
        return counts
