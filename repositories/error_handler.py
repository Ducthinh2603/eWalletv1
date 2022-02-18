class MissingInformation(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Information missing"

    def __str__(self):
        return "Information missing"


class AccountNotExist(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Account does not exist or no longer exist"

    def __str__(self):
        return "Account does not exist or no longer exist"


class TransactionNotExist(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Transaction does not exist"

    def __str__(self):
        return "Transaction does not exist"


class TransactionEnded(Exception):
    def __init__(self, details):
        self.details = details
        self.code = 400
        self.msg = "Transaction session is over"

    def __str__(self):
        return "Transaction session is over"


class TransactionUnauthorised(Exception):
    def __init__(self, details):
        self.details = details
        self.code = 400
        self.msg = "Transaction can not accomplish"

    def __str__(self):
        return "Transaction can not accomplish"


class Unauthorised(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Unauthorised"

    def __str__(self):
        return "Unauthorised"


class Unauthenticated(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Can not verify information, probably identity"

    def __str__(self):
        return "Can not verified identification"


class InvalidInformation(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Information may be compromised"

    def __str__(self):
        return "Information may be compromised"


class NegativeNumber(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "Amount can't be negative"

    def __str__(self):
        return "Amount can't be negative"


set_exception = (MissingInformation, AccountNotExist, Unauthenticated,
                 Unauthenticated, InvalidInformation, NegativeNumber,
                 TransactionEnded, TransactionUnauthorised, TransactionNotExist
                 )