from flask_restful import Resource
from flask import request
from repositories.merchant_repo import MerchantRepo
from viewers.merchant_viewer import MerchantViewer
from viewers.general_viewer import ErrorViewer
from repositories.error_handler import set_exception


class MerchantController(Resource):
    def post(self):
        rq = request.get_json()
        try:
            merchant = MerchantRepo.add_merchant(rq)
        except set_exception as e:
            response = ErrorViewer(e.msg)
            return response.__dict__, e.code
        else:
            return MerchantViewer.merchant_view(merchant)





