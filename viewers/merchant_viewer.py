

class MerchantViewer:
    @staticmethod
    def merchant_view(merchant):
        response = {
            "merchantName": merchant.merchant_name,
            "accountId": merchant.account_id,
            "merchantId": merchant.merchant_id,
            "apiKey": merchant.api_key,
            "merchantUrl": merchant.merchant_url
        }
        return response