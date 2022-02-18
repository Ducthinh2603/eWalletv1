from models.account_model import AccountModel

class AccountViewer:
    @staticmethod
    def account_view(account):
        response = {
            "accountType": account.account_type,
            "accountId": account.account_id,
            "balance": account.balance
        }
        return response
