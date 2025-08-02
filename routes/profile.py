from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import mysql, bcrypt
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from config import Config

bp = Blueprint('profile', __name__, url_prefix='/dashboard/profile')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bp.route('/personal-info/', methods=['GET', 'POST'])
def personal_info():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        if not phone_number.isdigit() or len(phone_number) < 10:
            flash("Nomor HP tidak valid", "danger")
            return redirect(url_for('profile.personal_info'))

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND email != %s", (email, session['email']))
        if cur.fetchone():
            flash("Email sudah digunakan", "danger")
            return redirect(url_for('profile.personal_info'))

        cur.execute("UPDATE users SET name = %s, email = %s, phone_number = %s WHERE email = %s",
                    (name, email, phone_number, session['email']))
        mysql.connection.commit()
        cur.close()

        session['name'] = name
        session['email'] = email
        session['phone_number'] = phone_number

        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('profile.personal_info'))

    return render_template('dashboard/profile/index.html')

@bp.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        flash('Tidak ada file yang dipilih', 'danger')
        return redirect(url_for('profile.personal_info'))

    file = request.files['photo']
    if file.filename == '' or not allowed_file(file.filename):
        flash('File tidak valid', 'danger')
        return redirect(url_for('profile.personal_info'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET photo = %s WHERE email = %s", (f'uploads/{filename}', session['email']))
    mysql.connection.commit()
    cur.close()

    session['photo'] = f'uploads/{filename}'
    flash('Foto profil berhasil diubah!', 'success')
    return redirect(url_for('profile.personal_info'))


# change account password 
@bp.route('/change-password', methods=['GET', 'POST'])
def change_account_password():
    # if 'logged_in' not in session or not session['logged_in']:
    #     flash('Silakan login terlebih dahulu', 'danger')
    #     return redirect(url_for('login'))

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
        return redirect(url_for('profile.change_account_password'))

    return render_template('dashboard/profile/changePassword/index.html')


# settings profile
@bp.route('/settings', methods=['GET', 'POST'])
def settings_profile():
    return render_template('dashboard/profile/settingsProfile/index.html')