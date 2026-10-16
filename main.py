"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from command.transaction_command import ApplyTransactionCommand, TransactionHistory


def main():
    print("=== Personal Finance Manager ===\n")

    balance = Balance.get_instance()
    balance.reset()
    balance.register_observer(PrintObserver())
    balance.register_observer(LowBalanceAlertObserver(threshold=200))

    history = TransactionHistory()

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    print("--- Applying transactions ---")
    for t in all_transactions:
        history.execute(ApplyTransactionCommand(balance, t))

    print(f"\n{balance.summary()}")

    print("\n--- Undoing last transaction ---")
    history.undo()
    print(balance.summary())

    print("\n--- Redoing last transaction ---")
    history.redo()
    print(balance.summary())

if __name__ == "__main__":
    main()
