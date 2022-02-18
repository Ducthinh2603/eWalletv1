from flask_restful import Resource
from flask import request
from repositories.account_repo import AccountRepo
from controllers.jwt_helper import jwt_required
from viewers.account_viewer import AccountViewer
from viewers.general_viewer import ErrorViewer
from repositories.error_handler import *


class AccountController(Resource):
    def post(self):
        rq = request.get_json()
        try:
            new_account = AccountRepo.add_account(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        return AccountViewer.account_view(new_account), 200


class AccountTokenController(Resource):
    def get(self, account_id):
        try:
            token = AccountRepo.get_token(account_id)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            return {"token": token}, 200


class AccountTopupController(Resource):
    @jwt_required("issuer")
    def post(self, account_id):
        rq = request.get_json()
        try:
            account = AccountRepo.topup_account(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            return AccountViewer.account_view(account), 200

