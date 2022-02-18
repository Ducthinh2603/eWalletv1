import functools
from flask import request
from repositories import error_handler
from viewers.general_viewer import ErrorViewer
from repositories import repositories_helper
from repositories.merchant_repo import MerchantRepo


def jwt_required(account_type):
    def decorate_func(func):
        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            try:
                rq = request.get_json()
                token = request.headers.getlist(key="Authorization")[0].split()[1]
            except error_handler.Unauthorised as e:
                response = ErrorViewer(e.msg)
                return response.__dict__, e.code
            else:
                account_id = repositories_helper.token_decode(token).get("accountId", None)
                if account_type == "merchant":
                    try:
                        merchant = MerchantRepo.get_merchant(account_id)
                    except error_handler.AccountNotExist as e:
                        response = ErrorViewer(e.msg)
                        return response.__dict__, e.code

                    api_key = merchant.api_key
                    try:
                        account_id_decode = repositories_helper.token_decode(token, api_key)["accountId"]
                    except error_handler.Unauthorised as e:
                        response = ErrorViewer(e)
                        return response.__dict__, e.code
                    if account_id_decode != account_id:
                        e = error_handler.Unauthenticated
                        response = ErrorViewer(e.msg)
                        return response.__dict__, e.code
                    else:
                        return func(*args, **kwargs)
                else:
                    if account_id == rq['accountId']:
                        return func(*args, **kwargs)
                    else:
                        e = error_handler.Unauthenticated()
                        response = ErrorViewer(e.msg)
                        return response.__dict__, e.code
        return decorated_func
    return decorate_func
