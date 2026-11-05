# Type Hint

# 1. Create four variables representing a merchant name, transaction count, transaction value, and whether the merchant is active. Add the correct type hints.

merchant_name : str = "ali"
transaction_count : int = 10
transaction_value:float = 20.00
account_active: bool = True


# 6. Write a function get_merchant_name() that takes a merchant name as a parameter and returns it. Add type hints.

def get_merchant_name(merchant_name: str) -> str:
    return merchant_name

# 7. Write a function add_transactions() that accepts two integers and returns their total. Add type hints.

def add_transactions(transaction_1: int, transaction_2: int) -> int:
    return transaction_1 + transaction_2


# 9. Write a function is_large_transaction() that accepts a transaction amount and returns True if it is greater than $1,000. Add type hints.

def is_large_transaction(transaction_amount: float) -> bool:
    return transaction_amount > 1000

# 10. Write a function calculate_fee() that accepts a transaction amount and a fee rate and returns the calculated fee. Add type hints.

def calculate_fee(transaction_amount: float, fee_rate: float) -> float:
    return transaction_amount * fee_rate


# 11. Create a function that accepts a merchant name, transaction count, and transaction value, then returns a formatted merchant summary as a string. Add type hints.

def merchant_summary(
    merchant_name: str,
    transaction_count: int,
    transaction_value: float
) -> str:
    return (
        f"Merchant: {merchant_name}, "
        f"Transactions: {transaction_count}, "
        f"Total Value: ${transaction_value}"
    )

# 12. Create a function that accepts a transaction amount and a boolean is_international. Calculate the fee differently depending on whether the transaction is international. Add type hints.

def calculate_fee(transaction_amount: float, is_international: bool) -> float:
    if is_international:
        return transaction_amount * 0.03
    else:
        return transaction_amount * 0.01

# 14. Create a function that accepts a merchant name, monthly revenue, and monthly cost and returns whether the merchant is profitable. Add type hints.

def is_profitable(
    merchant_name: str,
    monthly_revenue: float,
    monthly_cost: float
) -> bool:
    return monthly_revenue > monthly_cost

# 15. Take a function containing no type hints and add appropriate type annotations to every parameter and the return value.

def calculate_total(price: float, quantity: int) -> float:
    total: float = price * quantity
    return total


# Difficult
#
# 16. Create a function that accepts a merchant's transaction value, fee percentage, and fixed fee. Calculate and return the total fee. Add type hints to everything.

def calculate_total_fee(
        T_value: float,
        fee_percentage: float,
        fixed_fee: float
) -> float :
    total_value: float = (T_value * 0.7) + fixed_fee
    return total_value

