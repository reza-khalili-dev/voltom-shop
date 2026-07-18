import requests


class ZarinpalService:
    SANDBOX_URL = 'https://sandbox.zarinpal.com/pg/v4/payment'
    PRODUCTION_URL = 'https://api.zarinpal.com/pg/v4/payment'

    def __init__(self, merchant_id, sandbox=True):
        self.merchant_id = merchant_id
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL

    def create_payment(self, order_id, amount, callback_url, description=''):
        url = f'{self.base_url}/request.json'
        data = {
            'merchant_id': self.merchant_id,
            'amount': int(amount),
            'callback_url': callback_url,
            'description': description or f'سفارش شماره {order_id}',
        }
        try:
            response = requests.post(url, json=data, timeout=30)
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}

    def verify_payment(self, authority, amount):
        url = f'{self.base_url}/verify.json'
        data = {
            'merchant_id': self.merchant_id,
            'authority': authority,
            'amount': int(amount),
        }
        try:
            response = requests.post(url, json=data, timeout=30)
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}