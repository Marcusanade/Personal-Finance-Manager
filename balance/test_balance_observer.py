import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        t_income = Transaction(100, TransactionCategory.INCOME)
        self.balance.apply_transaction(t_income)
        self.assertFalse(observer.alert_triggered)

        t_expense = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t_expense)
        self.assertTrue(observer.alert_triggered)

        t_income2 = Transaction(100, TransactionCategory.INCOME)
        self.balance.apply_transaction(t_income2)
        self.assertFalse(observer.alert_triggered)

        t_expense2 = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t_expense2)
        self.assertFalse(observer.alert_triggered)

        t_expense3 = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t_expense3)
        self.assertTrue(observer.alert_triggered)


if __name__ == "__main__":
    unittest.main()
