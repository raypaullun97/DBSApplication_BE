from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'frontendAPI'
app.config['MYSQL_DATABASE_PASSWORD'] = 'DBSHackGroup12_API'
app.config['MYSQL_DATABASE_DB'] = 'bank'
app.config['MYSQL_DATABASE_HOST'] = '172.20.10.13'
mysql.init_app(app)