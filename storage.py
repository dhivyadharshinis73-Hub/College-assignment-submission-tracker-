import json
from pathlib import Path
from typing import List

from .models import Assignment


class AssignmentStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Assignment]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return [Assignment.from_dict(item) for item in data]

    def save(self, assignments: List[Assignment]) -> None:
        with self.file_path.open("w", encoding="utf-8") as handle:
            json.dump([assignment.to_dict() for assignment in assignments], handle, indent=2)
