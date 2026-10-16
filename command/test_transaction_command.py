import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from command.transaction_command import ApplyTransactionCommand, TransactionHistory


class TestCommandPattern(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.history = TransactionHistory()

    def test_execute_income(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.history.execute(ApplyTransactionCommand(self.balance, t))
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_income(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.history.execute(ApplyTransactionCommand(self.balance, t))
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_expense(self):
        t = Transaction(50, TransactionCategory.EXPENSE)
        self.history.execute(ApplyTransactionCommand(self.balance, t))
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo(self):
        t = Transaction(200, TransactionCategory.INCOME)
        self.history.execute(ApplyTransactionCommand(self.balance, t))
        self.history.undo()
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 200)

    def test_multiple_undo(self):
        self.history.execute(ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME)))
        self.history.execute(ApplyTransactionCommand(self.balance, Transaction(40, TransactionCategory.EXPENSE)))
        self.assertEqual(self.balance.get_balance(), 60)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 100)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
