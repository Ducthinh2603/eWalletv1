import copy

from controllers.jwt_helper import jwt_required
from flask_restful import Resource
from flask import request
from repositories import repositories_helper
from repositories.error_handler import *
from repositories.account_repo import AccountRepo
from repositories.merchant_repo import MerchantRepo
from repositories.transaction_repo import TransactionRepo
from viewers.transaction_viewer import TransactionViewer
from viewers.general_viewer import ErrorViewer
from threading import Thread


class CreateTransactionController(Resource):
    @jwt_required("merchant")
    def post(self):
        rq = request.get_json()
        try:
            merchant = MerchantRepo.get_merchant(merchant_info=rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        if repositories_helper.check_signature(merchant.api_key, **rq):
            try:
                transaction = TransactionRepo.create_transaction(rq)
            except set_exception as e:
                response = ErrorViewer(e.msg)
                return response.__dict__, e.code
            else:
                signature = repositories_helper.signature_generator(merchant.api_key,
                                                                    **transaction.__dict__)
                return TransactionViewer.transaction_view(transaction, signature), 200
        else:
            e = InvalidInformation()
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code


class ConfirmTransactionController(Resource):
    @jwt_required("personal")
    def post(self):
        rq = request.get_json()
        try:
            transaction = TransactionRepo.check_transaction(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            if transaction.outcome_account:
                e = TransactionUnauthorised('Payment process is occupied by another account')
                response = ErrorViewer(e.msg, e.details)
                return response.__dict__, e.code
            else:
                account_id = rq['accountId']
                rs = AccountRepo.get_account(account_id)
                if rs:
                    account_id = rs[0]
                    try:
                        TransactionRepo.confirm_transaction(transaction, account_id)
                    except set_exception as e:
                        response = ErrorViewer(e.msg, e.details)
                        return response.__dict__, e.code
                    else:
                        t = Thread(target=TransactionRepo.confirm_expire, args=(transaction.transaction_id,))
                        t.start()
                else:
                    e = AccountNotExist()
                    response = ErrorViewer(e.msg)
                    return response.__dict__, e.code


class VerifyTransactionController(Resource):
    @jwt_required("personal")
    def post(self):
        rq = request.get_json()
        try:
            TransactionRepo.verify_transaction(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            return {}, 200


class CancelTransactionController(Resource):
    @jwt_required('personal')
    def post(self):
        rq = request.get_json()
        try:
            TransactionRepo.cancel_transaction(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            return {}, 200
