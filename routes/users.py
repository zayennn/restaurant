from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import mysql, bcrypt
import MySQLdb.cursors

bp = Blueprint('users', __name__, url_prefix='/dashboard/users')

@bp.route('/')
def users():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()
    return render_template('dashboard/users/index.html', users=users)


@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm_password']
        role = request.form['role']

        # Validasi
        if password != confirm:
            flash("Password tidak cocok", "danger")
            return redirect(url_for('users.create_user'))

        if not phone.isdigit() or len(phone) < 10:
            flash("Nomor HP tidak valid", "danger")
            return redirect(url_for('users.create_user'))

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for('users.create_user'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute("""
            INSERT INTO users (name, email, phone_number, password, role)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, hashed_pw, role))
        mysql.connection.commit()
        cur.close()

        flash("Staff berhasil ditambahkan!", "success")
        return redirect(url_for('users.users'))

    return render_template('dashboard/users/create.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']

        cur.execute("""
            UPDATE users SET name=%s, email=%s, phone_number=%s, role=%s WHERE id=%s
        """, (name, email, phone, role, id))
        mysql.connection.commit()
        cur.close()

        flash('Data user berhasil diperbarui!', 'success')
        return redirect(url_for('users.users'))

    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('dashboard/users/edit.html', user=user)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('User berhasil dihapus!', 'success')
    return redirect(url_for('users.users'))