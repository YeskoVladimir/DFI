from typing import Any
from uuid import UUID

from models import Item, Action


class Transaction:
    def __init__(self, storage: list[Item], parent=None):
        self.storage = storage
        self.parent = parent
        self.backup: list[Item] = storage.copy()
        self.changes: list[tuple[Action, Any]] = []

    def insert(self, record: Item) -> None:
        self.changes.append((Action.insert, record))

    def delete(self, record_id: UUID) -> None:
        self.changes.append((Action.delete, record_id))

    def commit(self) -> list[Item]:
        if self.parent:
            self.parent.merge_changes(self.changes)
        else:
            for action, data in self.changes:
                if action == Action.insert:
                    self.backup.append(data)
                elif action == Action.delete:
                    self.backup = [
                        item for item in self.storage if item.id != data
                    ]

        self.changes.clear()
        return self.backup

    def rollback(self) -> None:
        self.changes.clear()

    def merge_changes(self, child_changes) -> None:
        self.changes.extend(child_changes)
