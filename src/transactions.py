from typing import Any
from uuid import UUID

from models import Item, Action


class TransactionException(Exception):
    pass


class Transaction:
    def __init__(self, storage: list[Item], parent=None):
        self.storage = storage
        self.parent = parent
        self.changes: list[tuple[Action, Any]] = []
        self.active_child: list[UUID] = []

    def insert(self, record: Item) -> None:
        self.changes.append((Action.insert, record))

    def delete(self, record_id: UUID) -> None:
        self.changes.append((Action.delete, record_id))

    def commit(self, transaction_id: UUID) -> list[Item] | None:
        if self.parent:
            self.parent.merge_changes(self.changes)
            self.parent.active_child.remove(transaction_id)
            return None
        else:
            backup: list[Item] = self.storage.copy()
            for action, data in self.changes:
                try:
                    if action == Action.insert:
                        backup.append(data)
                    elif action == Action.delete:
                        backup = [
                            item for item in self.storage if item.id != data
                        ]
                except Exception:
                    raise TransactionException
            self.changes.clear()
            return backup

    def rollback(self) -> None:
        self.changes.clear()

    def merge_changes(self, child_changes) -> None:
        self.changes.extend(child_changes)
