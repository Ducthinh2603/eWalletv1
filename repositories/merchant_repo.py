import sqlite3
from models.merchant_model import MerchantModel
from repositories.account_repo import AccountRepo
from repositories import repositories_helper,error_handler


class MerchantRepo:
    @staticmethod
    def get_merchant(account_id=None, merchant_info=None):
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            if account_id:
                qr_account_id = '''
                    SELECT * FROM Merchant WHERE account_id = (?)
                '''
                c.execute(qr_account_id, (account_id,))
            elif merchant_info:
                try:
                    merchant_id = merchant_info['merchantId']
                except Exception:
                    raise error_handler.MissingInformation
                qr_merchant_id = '''
                    SELECT * FROM Merchant WHERE merchant_id = (?)
                '''
                c.execute(qr_merchant_id, (merchant_id,))
            rs = c.fetchone()
            if rs:
                return MerchantModel(*rs)
            else:
                raise error_handler.AccountNotExist


    @staticmethod
    def get_api_key(account_id):
        qr = '''
            SELECT api_key FROM Merchant WHERE account_id = (?)
        '''
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(qr, (account_id,))
            rs = c.fetchone()
            if rs:
                return rs[0]
            return None

    @staticmethod
    def add_merchant(rq):
        try:
            merchant_name = rq["merchantName"]
            merchant_url = rq['merchantUrl']
        except Exception:
            raise error_handler.MissingInformation
        else:
            new_account = AccountRepo.add_account({"accountType":"merchant"})
            account_id = new_account.account_id
            merchant_id = repositories_helper.uuid_generator()
            api_key = repositories_helper.uuid_generator()
            add_merchant_qr = '''
                INSERT INTO Merchant VALUES (?,?,?,?,?)
                '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                c.execute(add_merchant_qr, (merchant_id, merchant_name,
                                            merchant_url, account_id, api_key))
                return MerchantModel(merchant_id, merchant_name,
                                     merchant_url, account_id, api_key)
