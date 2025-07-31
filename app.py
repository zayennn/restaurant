from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_restaurant_flask'

mysql = MySQL(app)
bcrypt = Bcrypt(app)


# middleware
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Silakan login dulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('Kamu tidak punya akses ke halaman ini.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator



# authentications
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # ← penting!
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['email'] = user['email']
            session['name'] = user['name']
            session['phone_number'] = user['phone_number']
            session['role'] = user['role']

            flash('Anda berhasil login!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau password salah', 'danger')
    return render_template('auth/login.html')


# register
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
        # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for('register'))
        
        cur.execute("""
            INSERT INTO users (name, phone_number, email, password, role)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone_number, email, hashed_password, 'user'))

        
        mysql.connection.commit()
        flash("Akun anda berhasil dibuat!", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Anda berhasil logout!", "success")
    return redirect(url_for('login'))


# dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')


# users
@app.route('/dashboard/users')
def users():
    return render_template('dashboard/users/index.html')


# seats
@app.route('/dashboard/seats')
def seats():
    return render_template('dashboard/seats/index.html')


# menus
@app.route('/dashboard/menus')
def menus():
    return render_template('dashboard/menus/index.html')


# reservations
@app.route('/dashboard/reservations')
def reservations():
    return render_template('dashboard/reservations/index.html')


# profile
@app.route('/dashboard/profile/personal-info')
def profile():
    return render_template('dashboard/profile/index.html')

# change account password 
@app.route('/dashboard/profile/change-password', methods=['GET', 'POST'])
def change_account_password():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Silakan login terlebih dahulu', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            flash('Semua field harus diisi', 'danger')
            return render_template('dashboard/profile/changePassword/index.html')

        if new_password != confirm_password:
            flash('Konfirmasi password tidak sesuai!', 'danger')
            return render_template('dashboard/profile/changePassword/index.html')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT password FROM users WHERE email = %s", (session['email'],))
        user = cur.fetchone()
        cur.close()

        if not user or not bcrypt.check_password_hash(user['password'], current_password):
            flash('Password lama tidak sesuai!', 'danger')
            return render_template('dashboard/profile/changePassword/index.html')

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s", 
                   (hashed_password, session['email']))
        mysql.connection.commit()
        cur.close()

        flash('Password berhasil diubah!', 'success')
        # return redirect(url_for('change_account_password'))

    return render_template('dashboard/profile/changePassword/index.html')

# profile settings
@app.route('/dashboard/profile/settings', methods=['GET', 'POST'])
def profile_settings():
    return render_template('dashboard/profile/settingsProfile/index.html')


if __name__ == '__main__':
    app.run(debug=True)