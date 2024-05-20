import uuid
from uuid import UUID

from fastapi import HTTPException

from models import Item
from transactions import Transaction


class Service:
    def __init__(self):
        self.storage: list[Item] = []
        self.transactions: dict[UUID, Transaction] = {}

    def select(self) -> list[Item]:
        return self.storage

    def insert(self, value: str, transaction_id: UUID) -> UUID:
        transaction = self._get_transaction(transaction_id)
        value_id = uuid.uuid4()
        transaction.insert(Item(id=value_id, value=value))
        return value_id

    def delete(self, value_id: UUID, transaction_id: UUID) -> None:
        transaction = self._get_transaction(transaction_id)
        transaction.delete(value_id)

    def begin(self, parent_id: UUID | None) -> UUID:
        transaction_id = uuid.uuid4()

        if not parent_id:
            transaction = Transaction(storage=self.storage)
            self.transactions[transaction_id] = transaction

            return transaction_id

        parent = self._get_transaction(transaction_id)

        transaction = Transaction(storage=self.storage, parent=parent)
        self.transactions[transaction_id] = transaction

        return transaction_id

    def commit(self, transaction_id: UUID) -> None:
        transaction = self._get_transaction(transaction_id)
        new_storage = transaction.commit()
        self.storage = new_storage
        del self.transactions[transaction_id]

    def rollback(self, transaction_id: UUID) -> None:
        transaction = self._get_transaction(transaction_id)
        transaction.rollback()

    def _get_transaction(self, transaction_id: UUID) -> Transaction:
        if not (transaction := self.transactions.get(transaction_id)):
            raise HTTPException(
                status_code=404, detail="Transaction not found."
            )
        return transaction
