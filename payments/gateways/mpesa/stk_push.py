# payments/gateways/mpesa/stk_push.py

import requests
from datetime import datetime
import base64
import os

class MpesaSTKPush:
    def __init__(self, shortcode, passkey, consumer_key, consumer_secret, callback_url):
        self.shortcode = shortcode
        self.passkey = passkey
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_url = callback_url
        self.token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def get_access_token(self):
        response = requests.get(
            self.token_url,
            auth=(self.consumer_key, self.consumer_secret)
        )
        return response.json().get("access_token")

    def generate_password(self, timestamp):
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        encoded = base64.b64encode(data_to_encode.encode())
        return encoded.decode("utf-8")

    def initiate_payment(self, phone_number, amount, account_reference="Ref001", transaction_desc="Payment"):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = self.generate_password(timestamp)
        access_token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        response = requests.post(self.stk_url, json=payload, headers=headers)
        return response.json()
