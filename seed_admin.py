from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_restaurant_flask'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

with app.app_context():
    # data admin default
    name = "Admin"
    email = "admin@example.com"
    phone_number = "081234567890"
    password = "admin123"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    role = "admin"

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing = cur.fetchone()

    if existing:
        print("✅ Admin sudah ada.")
    else:
        cur.execute("""
            INSERT INTO users (name, phone_number, email, password, role)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone_number, email, hashed_password, role))
        mysql.connection.commit()
        print("✅ Admin berhasil dibuat.")

    cur.close()