import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

		
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


@app.route("/details/<string:accountId>", methods=["POST"])
def get_account_details(userID):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM BankAccount WHERE UserId=%s", int(UserID))
		row = cursor.fetchone()
		resp = jsonify(row)
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