# Reflection — Personal Finance Manager

## Design Patterns Used

**Singleton (Balance)**
I used the Singleton pattern to manage the balance because there should only ever be one source of truth for the user's funds. This ensures that there is only one object with the same data.

**Adapter (TransactionAdapter)**
The freelance platform provides income data in its own format (`ExternalFreelanceIncome`), which is incompatible with the app's `Transaction` class. The Adapter wraps the external object and converts it without modifying either class — useful when integrating third-party data sources you don't control.

**Observer (LowBalanceAlertObserver, PrintObserver)**
I used the Observer pattern to notify subscribers whenever the balance changes. This keeps the `Balance` class decoupled from the notification logic — adding a new alert type only requires creating a new observer and registering it, with no changes to `Balance` itself. It is essentially the same mechanism as webhooks in real-world APIs.

**Command (ApplyTransactionCommand, TransactionHistory)**
The Command pattern wraps each transaction in an object that knows how to execute and undo itself. This made it straightforward to add undo/redo functionality without touching the `Balance` class. The main trade-off is added complexity. For a simple app this may be overkill, but it pays off when the history of actions matters.

## How patterns improved the design and trade-offs

Each pattern reduced coupling and made the app easier to extend. Using well-known patterns also improves readability: any Python developer familiar with these standard patterns can understand the intent of each component without reading all the code. The main trade-off is added complexity. For a small app like this the extra boilerplate may not be justified, and as a newcomer to design patterns I found that applying all four at once added a significant learning curve. However, it pays off in testability and maintainability as the project grows.
