import sqlite3
from models.account_model import AccountModel
from repositories import repositories_helper, error_handler
import jwt


class AccountRepo:

    @staticmethod
    def get_account(account_id):
        get_account_qr = '''
            SELECT * FROM Account WHERE account_id = (?)
        '''
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(get_account_qr, (account_id,))
            rs = c.fetchone()
            return rs

    @staticmethod
    def add_account(rq):
        try:
            account_type = rq["accountType"]
        except Exception:
            raise error_handler.MissingInformation
        else:
            add_account_qr = '''
                INSERT INTO Account VALUES (?,?,0)
            '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                account_id = repositories_helper.uuid_generator()
                c.execute(add_account_qr, (account_id, account_type))
                return AccountModel(account_id, account_type, 0)

    @staticmethod
    def get_token(account_id):
        _id = AccountRepo.get_account(account_id)
        if _id:
            if _id[1] == "merchant":
                get_key_qr = '''
                    SELECT api_key FROM Merchant WHERE account_id = (?)
                '''
                with sqlite3.connect(repositories_helper.DBPATH) as conn:
                    c = conn.cursor()
                    c.execute(get_key_qr, (_id[0],))
                    api_key = c.fetchone()[0]
                token = jwt.encode({"accountId": _id[0]}, api_key, algorithm="HS256")
            elif _id[1] == "personal":
                token = jwt.encode({"accountId": _id[0]}, "secret", algorithm="HS256")
            return token
        else:
            raise error_handler.AccountNotExist

    @staticmethod
    def topup_account(rq):
        try:
            account_id = rq["accountId"]
            amount = rq["amount"]
        except KeyError:
            raise error_handler.MissingInformation
        else:
            if amount < 0:
                raise error_handler.NegativeNumber
            topup_qr = '''
                UPDATE Account SET balance = balance + (?) WHERE account_id = (?)
            '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                try:
                    c.execute(topup_qr, (amount, account_id))
                except Exception:
                    raise error_handler.AccountNotExist
            account = AccountRepo.get_account(account_id)
            return AccountModel(*account)
