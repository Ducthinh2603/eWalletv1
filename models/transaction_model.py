import enum


class TransactionStatus(enum.Enum):
    INITIALIZED = 1
    COMFIRMED = 2
    VERIFIED = 3
    COMPLETED = 4
    CANCELED = 5
    EXPIRED = 6
    FAILED = 7


class TransactionModel:
    def __init__(self, transaction_id, merchant_id,
                 income_account, outcome_account,
                 amount, extra_data, status):
        self.transaction_id = transaction_id
        self.merchant_id = merchant_id
        self.income_account = income_account
        self.outcome_account = outcome_account
        self.amount = amount
        self.extra_data = extra_data
        self.status = status






