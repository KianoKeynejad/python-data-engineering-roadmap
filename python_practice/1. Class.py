# ## Python Classes & Objects — Practice Questions

# 1. Create a `Merchant` class with an `__init__()` method that stores a merchant's `name` and `industry` as instance attributes.

class Merchant :
    def __init__(self, name, industry):
        self.name = name
        self.industry = industry

# 2. Create two different `Merchant` objects and print each merchant's name and industry.

merchant1 = Merchant("ABC Cafe", "Restaurant")
merchant2 = Merchant("XYZ Bakery", "Bakery")

# 3. Create a `Transaction` class that stores `amount` and `payment_method` as instance attributes. Create one transaction object and print its attributes.

class Transaction:
    def __init__(self, amount: float, payment_method: str):
        self.amount = amount
        self.payment_method = payment_method

transaction1 = Transaction(100.50, "debit")

print(transaction1.amount)
print(transaction1.payment_method)


# 4. Add an instance method called `display_transaction()` to the `Transaction` class that prints the transaction's amount and payment method.


class Transaction:
    def __init__(self, amount: float, payment_method: str):
        self.amount = amount
        self.payment_method = payment_method

    def display_transaction(self) -> None:
        print(f"Amount : {self.amount}")
        print(f"Payment_method  :  {self.payment_method}")

transaction1 = Transaction(100.50, "debit")

transaction1.display_transaction()

# 5. Create a `FeeCalculator` class that stores a `fee_rate` when the object is created. Add an instance method that accepts a transaction amount and calculates the fee.

class FeeCalculator:
    def __init__ (self, fee_rate:float):
        self.fee_rate = fee_rate

    def calculate_fee(self, transaction_amount: float) -> float:
        return transaction_amount * self.fee_rate

fee_calculator = FeeCalculator(0.02)
fee = fee_calculator.calculate_fee(500)
print(fee)

# 6. Create a `Merchant` class that stores `name`, `monthly_ttv`, and `is_active`. Add an instance method called `is_large_merchant()` that determines whether the merchant's monthly TTV is greater than `$100,000`.

class Merchant:
    def __init__ (self, name: str, monthly_TTV: float, is_active: bool):
        self.name = name
        self.monthly_TTV = monthly_TTV
        self.is_active = is_active

    def is_large_merchant (self) -> bool:
        return self.monthly_TTV > 100000

merchant1 = Merchant("ABC Cafe", 125000.00, True)
print(merchant1.is_large_merchant())


# 8. Create a `Merchant` class with `name` and `transaction_count`. Add an instance method that increases the transaction count by one whenever a new transaction is processed.

class Merchant:
    def __init__ ( self, name: str, transaction_count: int):
        self.name = name
        self.transaction_count = transaction_count

    def add_transaction(self) -> None:
        self.transaction_count +=  1

merchant1 = Merchant("ABC Cafe", 125000.00)

merchant1.add_transaction()

print(merchant1.transaction_count)

# ### Difficult
#
# 9. Create a `Transaction` class with `transaction_id`, `merchant_name`, `amount`, and `payment_method`. Add an instance method that returns a formatted transaction summary.

class Transaction:
    def __init__ (self, transaction_id: str, merchant_name: str, amount: float, payment_method: str):
        self.transaction_id = transaction_id
        self.merchant_name = merchant_name
        self.amount = amount
        self.payment_method = payment_method

    def display_transaction(self) -> str:
        return \
            (f"Transaction id : {self.transaction_id},"
            f"merchant name : {self.merchant_name},"
            f"amount : {self.amount},"
            f"payment method : {self.payment_method}"
        )


# 10. Create a `Merchant` class with `name`, `monthly_revenue`, and `monthly_cost`. Add an instance method that calculates the merchant's profit and another method that determines whether the merchant is profitable.

class Merchant:

    def __init__(
        self,
        name: str,
        monthly_revenue: float,
        monthly_cost: float
    ):
        self.name = name
        self.monthly_revenue = monthly_revenue
        self.monthly_cost = monthly_cost

    def calculate_profit(self) -> float:
        return self.monthly_revenue - self.monthly_cost

    def is_profitable(self) -> bool:
        return self.calculate_profit() > 0


merchant1 = Merchant("ABC Cafe", 15000.00, 10000.00)

print(merchant1.calculate_profit())
print(merchant1.is_profitable())

