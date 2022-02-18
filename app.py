from flask import Flask
from flask_restful import Api
from controllers import account_controller, merchant_controller, transaction_controller

app = Flask(__name__)
api = Api(app)

api.add_resource(account_controller.AccountController, '/account')
api.add_resource(account_controller.AccountTokenController, '/account/<account_id>/token')
api.add_resource(account_controller.AccountTopupController, '/account/<account_id>/topup')
api.add_resource(merchant_controller.MerchantController, '/merchant/signup')
api.add_resource(transaction_controller.CreateTransactionController, '/transaction/create')
api.add_resource(transaction_controller.ConfirmTransactionController, '/transaction/confirm')
api.add_resource(transaction_controller.VerifyTransactionController, '/transaction/verify')
api.add_resource(transaction_controller.CancelTransactionController, '/transaction/cancel')

if __name__ == '__main__':
    app.run(port=3000, debug=True)



