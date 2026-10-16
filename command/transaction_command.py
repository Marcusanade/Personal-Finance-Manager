from abc import ABC, abstractmethod
from transaction.transaction_category import TransactionCategory


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class ApplyTransactionCommand(Command):
    """Applies a transaction to the balance and supports undo."""

    def __init__(self, balance, transaction):
        self._balance = balance
        self._transaction = transaction

    def execute(self):
        self._balance.apply_transaction(self._transaction)

    def undo(self):
        # Reverse the transaction: income → expense, expense → income
        if self._transaction.category == TransactionCategory.INCOME:
            self._balance.add_expense(self._transaction.amount)
        else:
            self._balance.add_income(self._transaction.amount)


class TransactionHistory:
    """Invoker: executes commands and manages undo/redo history."""

    def __init__(self):
        self._history = []
        self._redo_stack = []

    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self):
        if not self._history:
            print("Nothing to undo.")
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        if not self._redo_stack:
            print("Nothing to redo.")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
