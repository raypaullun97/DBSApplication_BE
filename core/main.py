import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
		
		
@app.route('/transaction/<int:a_id>')
def transaction(a_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT TransactionID t_id, AccountID a_id, Date date, TransactionAmount amt, Comment comment FROM scheduledtransactions WHERE AccountID=%s", a_id)
		row = cursor.fetchone()
		resp = jsonify(row)
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