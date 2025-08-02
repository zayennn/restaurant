from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import mysql, bcrypt
import MySQLdb.cursors

def create_login_session(user):
    session['logged_in'] = True
    session['email'] = user['email']
    session['name'] = user['name']
    session['phone_number'] = user['phone_number']
    session['role'] = user['role']
    session['photo'] = user.get('photo') or 'uploads/default.png'

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            create_login_session(user)
            flash('Anda berhasil login!', 'success')
            if user['role'] in ['admin', 'petugas']:
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('seats.seats'))
        else:
            flash('Email atau password salah', 'danger')

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Password tidak cocok", "danger")
            return redirect(url_for('auth.register'))

        if not phone_number.isdigit() or len(phone_number) < 10:
            flash("Nomor HP tidak valid", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing = cur.fetchone()

        if existing:
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for('auth.register'))

        cur.execute("INSERT INTO users (name, phone_number, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                    (name, phone_number, email, hashed_password, 'user'))
        mysql.connection.commit()
        flash("Akun anda berhasil dibuat!", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash("Anda berhasil logout!", "success")
    return redirect(url_for('auth.login'))