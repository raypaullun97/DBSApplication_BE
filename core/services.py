from flask import Flask
from core import app



db = app.db
class UserService:
    def login(self, credentials):
        # user = User.query.filter_by( user_id = credentials['user_id'],
        #                              password = credentials['password']).first()
        
        return { "UserID": 1,
                "Username": "ExecutiveDBS",
                "Password": "DBSBestBank2022",
                "Firstname": "Tom",
                "Lastname": "Lim",
                "Email": "TomLim@easymail.com",
                "Address": "Block 123 Serangoon Garden #10-129",
                "OptIntoPhyStatements": 0
            }