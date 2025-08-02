from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import mysql
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from datetime import datetime

bp = Blueprint('menus', __name__, url_prefix='/dashboard/menus')

UPLOAD_FOLDER = 'static/uploads/menus'

@bp.route('/')
def menus():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM menus")
    menus = cur.fetchall()
    cur.close()
    return render_template('dashboard/menus/index.html', menus=menus)

@bp.route('/create', methods=['GET', 'POST'])
def create_menu():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        qty = request.form['qty']

        # Handle image
        image_file = request.files['menu_image']
        image_filename = ''
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO menus (name, description, price, category, qty, image) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, description, price, category, qty, image_filename))
        mysql.connection.commit()
        cur.close()

        flash('Menu created successfully!', 'success')
        return redirect(url_for('menus.menus'))
    return render_template('dashboard/menus/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        qty = request.form['qty']

        # Cek apakah ada gambar baru
        image_file = request.files['menu_image']
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image_file.save(image_path)
            cur.execute("UPDATE menus SET name=%s, description=%s, price=%s, category=%s, qty=%s, image=%s WHERE id=%s",
                        (name, description, price, category, qty, image_filename, id))
        else:
            cur.execute("UPDATE menus SET name=%s, description=%s, price=%s, category=%s, qty=%s WHERE id=%s",
                        (name, description, price, category, qty, id))

        mysql.connection.commit()
        cur.close()

        flash('Menu updated successfully!', 'success')
        return redirect(url_for('menus.menus'))

    cur.execute("SELECT * FROM menus WHERE id=%s", (id,))
    menu = cur.fetchone()
    cur.close()
    return render_template('dashboard/menus/edit.html', menu=menu)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_menu(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM menus WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Menu deleted successfully!', 'success')
    return redirect(url_for('menus.menus'))