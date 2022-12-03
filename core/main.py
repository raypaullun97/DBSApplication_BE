import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from flask_jwt import JWT,current_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

@app.route('/account/login', methods=['POST'])
def login():
	try:
		_json = request.get_json()
		_username = _json['credentials']['username']
		_password = _json['credentials']['password']
		if _username and _password and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(f"SELECT * FROM User WHERE Username=%s and Password=%s",( _username, _password,))
			row = cursor.fetchone()
			if row != None:
				login_limit = 3
				show_alert = False
				login_count = row['LoginCount'] + 1
				user_id = row['UserID']
				if login_count < login_limit:
					cursor.execute("UPDATE User SET LoginCount=%s WHERE UserID=%s", (login_count, user_id,))
				else:
					cursor.execute("UPDATE User SET LoginCount=0 WHERE UserID=%s", user_id)
					show_alert = True
				conn.commit()
				access_token = create_access_token(identity=_username)
				resp = jsonify({
					"code": 200,
					"data": "Login successful.",
					"access_token": access_token, 
					"show_alert": show_alert
				})
			else:
				resp = jsonify({
					"code": 401,
					"data": "Either your username or password is wrong."
				})
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/account/user_details/<int:u_id>', methods=['GET'])
def get_user_details(u_id):
	print(u_id)
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT UserID, Firstname, Lastname, Email, Address FROM User WHERE UserID=%s", u_id)
		row = cursor.fetchone()
		if row != None:
			resp = jsonify(row)
		else:
			resp = jsonify("User not found")
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/account/update_details', methods=['POST'])
def update_user_details():
	try:
		_json = request.get_json()
		_userID = _json['userID']
		_email = _json['email']
		_address = _json['address']
		if _userID and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT UserID, Firstname, Lastname, Email, Address FROM User WHERE UserID=%s", _userID)
			row = cursor.fetchone()
			if row != None:
				cursor.execute("UPDATE User SET Address=%s, Email=%s WHERE UserID=%s",( _address, _email, _userID, ))
				conn.commit()
				resp = jsonify({
					"code": 200,
					"data": "Update successful."
				})
			else:
				resp = jsonify("Unable to update details.")
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
		return resp
	finally:
		cursor.close()
		conn.close()

@app.route('/transaction/<int:a_id>')
def transaction(a_id):
	try:
		transaction_list = {}
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT TransactionID t_id, AccountID a_id, Date date, TransactionAmount amt, Comment comment FROM scheduledtransactions WHERE AccountID=%s", a_id)
		rows = cursor.fetchall()
		resp = jsonify(transaction_list)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/addtransaction', methods=['POST'])
def addtransaction():
	try:
		_json = request.json
		_TransactionAmount = _json['TransactionAmount']
		_Comment = _json['Comment']
		_AccountID = _json['AccountID']
		_ReceivingAccountID = _json['ReceivingAccountID']
		_Date = _json['Date']
		# validate the received values
		if _TransactionAmount and _Comment and _AccountID and _ReceivingAccountID and _Date and request.method == 'POST':
			sql = "INSERT INTO scheduledtransactions(AccountID, ReceivingAccountID, Date, TransactionAmount, Comment) VALUES(%s, %s, %s, %s, %s)"
			data = (_AccountID, _ReceivingAccountID, _Date, _TransactionAmount, _Comment,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Transaction added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route("/details", methods=["POST"])
@jwt_required()
def get_account_details():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()
	try:
		_json = request.get_json()
		_userId = _json['credentials']['userId']
		# _password = _json['credentials']['access_token']
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM BankAccount WHERE UserId=%s", int(_userId))
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@app.route('/ft/<int:id>',methods=["DELETE"])
def deleteFutureTrans(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("DELETE FROM scheduledtransactions WHERE TransactionID=%s", (id,))
		conn.commit()
		resp = jsonify('Transection deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()