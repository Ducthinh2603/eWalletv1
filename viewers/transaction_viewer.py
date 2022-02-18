from repositories import repositories_helper


class TransactionViewer:
    @staticmethod
    def transaction_view(transaction, signature):
        # transaction = TransactionModel(*rs)
        response = {
            "transactionId": transaction.transaction_id, "merchantId": transaction.merchant_id,
            "incomeAccount": transaction.income_account,
            "outcomeAccount": transaction.outcome_account if transaction.outcome_account else "NULL",
            "amount": transaction.amount,
            "extraData": transaction.extra_data, "status": transaction.status,
            'signature': signature
        }
        return response
