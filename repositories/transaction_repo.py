import sqlite3
from models.transaction_model import TransactionModel, TransactionStatus
from repositories.account_repo import AccountRepo
from repositories import repositories_helper
import time
from repositories import error_handler


class TransactionRepo:
    @staticmethod
    def check_transaction(rq):
        try:
            _id = rq['accountId']
            transaction_id = rq['transactionId']
        except Exception:
            raise error_handler.MissingInformation
        else:
            _ = AccountRepo.get_account(_id)
            rs = TransactionRepo.get_transaction(transaction_id)
            if rs:
                return TransactionModel(*rs)
            else:
                raise error_handler.TransactionNotExist

    @staticmethod
    def check_transaction_valid(transaction_id, phase=TransactionStatus.COMPLETED, check_ended=False):
        current_status = TransactionRepo.get_status_transaction(transaction_id)
        if check_ended:
            if TransactionStatus(current_status).value >= TransactionStatus.COMPLETED.value:
                return True
            return False
        else:
            if phase.value - 1 == current_status:
                return True
            raise error_handler.TransactionUnauthorised(f"The transacion is in "
                                                    f"{TransactionStatus(current_status).name} phase")

    @staticmethod
    def get_transaction(transaction_id):
        qr = '''
            SELECT * FROM Playbook WHERE transaction_id = (?)
        '''
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(qr, (transaction_id,))
            rs = c.fetchone()
            return rs

    @staticmethod
    def create_transaction(rq):
        try:
            merchant_id = rq["merchantId"]
            amount = rq["amount"]
            extra_data = rq.get("extraData", None)
        except Exception:
            raise error_handler.MissingInformation
        check_merchant = '''
            SELECT account_id FROM Merchant WHERE merchant_id = (?)
        '''
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(check_merchant, (merchant_id,))
            rs = c.fetchone()
            if rs:
                income_account = rs[0]
                outcome_account = None
                transaction_id = repositories_helper.uuid_generator()
                status = TransactionStatus.INITIALIZED.value
                create_qr = '''
                    INSERT INTO Playbook VALUES (?, ?, ?, NULL, ?, ?, ?)
                '''
                c.execute(create_qr, (transaction_id, merchant_id,
                                      income_account, amount, extra_data, status))
                return TransactionModel(transaction_id, merchant_id,
                                        income_account, outcome_account,
                                        amount, extra_data, status)
            else:
                raise error_handler.AccountNotExist

    @staticmethod
    def get_status_transaction(transaction_id):
        status_check = '''
            SELECT status FROM Playbook WHERE transaction_id = (?)
        '''
        with sqlite3.connect(repositories_helper.DBPATH) as conn:
            c = conn.cursor()
            c.execute(status_check, (transaction_id,))
            rs = c.fetchone()
            return rs[0]

    @staticmethod
    def confirm_transaction(transaction: TransactionModel, account_id):
        if TransactionRepo.check_transaction_valid(transaction.transaction_id, TransactionStatus.COMFIRMED):
            qr = '''
                UPDATE Playbook SET outcome_account = (?), status = (?) WHERE transaction_id = (?)
                '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                c.execute(qr, (account_id, TransactionStatus.COMFIRMED.value, transaction.transaction_id))
        else:
            raise error_handler.TransactionEnded

    @staticmethod
    def confirm_expire(transaction_id):
        time.sleep(60 * 30)
        if TransactionRepo.check_transaction_valid(transaction_id, check_ended=True):
            qr = '''
                UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
            '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                c.execute(qr, (TransactionStatus.EXPIRED.value, transaction_id))

    @staticmethod
    def verify_transaction(rq):
        transaction = TransactionRepo.check_transaction(rq)
        account_id = rq["accountId"]
        if TransactionRepo.check_transaction_valid(transaction.transaction_id, phase=TransactionStatus.VERIFIED):
            balance_qr = '''
                SELECT balance FROM Account WHERE account_id = (?)
            '''
            amount_qr = '''
                SELECT amount FROM Playbook WHERE transaction_id = (?)
            '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                c.execute(balance_qr, (account_id,))
                balance = c.fetchone()[0]
                c.execute(amount_qr, (transaction.transaction_id,))
                amount = c.fetchone()[0]
                update_transaction_qr = '''
                    UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
                '''
                if balance >= amount:
                    update_account_qr = '''
                        UPDATE Account SET balance = (?) WHERE account_id = (?)
                    '''
                    c.execute(update_account_qr, (balance - amount, account_id))
                    c.execute(update_transaction_qr, (TransactionStatus.COMPLETED.value, transaction.transaction_id))
                else:
                    c.execute(update_transaction_qr, (TransactionStatus.FAILED.value, transaction.transaction_id))
                    raise error_handler.TransactionUnauthorised("Not enough money in your wallet")

    @staticmethod
    def cancel_transaction(rq):
        transaction = TransactionRepo.check_transaction(rq)
        if TransactionRepo.check_transaction_valid(transaction.transaction_id, check_ended=True):
            qr = '''
                UPDATE Playbook SET status = (?) WHERE transaction_id = (?)
            '''
            with sqlite3.connect(repositories_helper.DBPATH) as conn:
                c = conn.cursor()
                c.execute(qr, (repositories_helper.CANCELED, transaction.transaction_id))
