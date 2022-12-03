import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash

@app.route('/account/login', methods=['POST'])
def login():
    try:
        _json = request.get_json()
        _username = _json['credentials']['username']
        _password = _json['credentials']['password']
        if _username and _password and request.method == 'POST':
            # _hashed_password = generate_password_hash(_password)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM User WHERE Username=%s and Password=%s",( _username, _password,))
            # data = (_username, _password,)
            row = cursor.fetchone()
            print(row)
            if row != None:
                resp = jsonify({
                    "code": 200,
                    "data": "Login successful."
                })
            else:
                return jsonify({
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