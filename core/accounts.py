from flask import Flask
from core import app

db = app.db

class AccountService:
    def account_details_service(self, userid):
        # user = User.query.filter_by( user_id = credentials['user_id'],
        #                              password = credentials['password']).first()

        return {
            "AccountID": 621156213,
            "UserID": 1,
            "AccountType": "Saving",
            "AcccountBalance": 70200.71
        }