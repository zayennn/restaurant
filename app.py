from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_restaurant_flask'

mysql = MySQL(app)
bcrypt = Bcrypt(app)


# authentications
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[4], password):
            session['logged_in'] = True
            session['email'] = user[1]
            flash('Login berhasil', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau password salah', 'danger')
    return render_template('auth/login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']
        
        if password != confirm:
            flash("Password tidak cocok", "danger")
            return redirect(url_for('register'))
        
        if not phone_number.isdigit() or len(phone_number) < 10:
            flash("Nomor HP tidak valid", "danger")
            return redirect(url_for('register'))

        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for('register'))
        
        cur.execute("INSERT INTO users (name, phone_number, email, password) VALUES (%s, %s, %s, %s)", 
            (name, phone_number, email, hashed_password))
        
        mysql.connection.commit()
        flash("Login berhasil", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("And berhasil logout!", "success")
    return redirect(url_for('login'))


# dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')


if __name__ == '__main__':
    app.run(debug=True)