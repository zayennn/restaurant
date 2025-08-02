from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import mysql
import MySQLdb.cursors

bp = Blueprint('seats', __name__, url_prefix='/dashboard/seats')

@bp.route('/')
def seats():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM seats")
    seats = cur.fetchall()
    cur.close()
    return render_template('dashboard/seats/index.html', seats=seats)

@bp.route('/create', methods=['GET', 'POST'])
def create_seat():
    if request.method == 'POST':
        name = request.form['name']
        capacity = request.form['capacity']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO seats (name, capacity, status) VALUES (%s, %s, %s)",
                    (name, capacity, status))
        mysql.connection.commit()
        cur.close()

        flash('Seat berhasil ditambahkan!', 'success')
        return redirect(url_for('seats.seats'))

    return render_template('dashboard/seats/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_seat(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        capacity = request.form['capacity']
        status = request.form['status']

        cur.execute("UPDATE seats SET name = %s, capacity = %s, status = %s WHERE id = %s",
                    (name, capacity, status, id))
        mysql.connection.commit()
        cur.close()
        flash('Seat berhasil diupdate!', 'success')
        return redirect(url_for('seats.seats'))

    cur.execute("SELECT * FROM seats WHERE id = %s", (id,))
    seat = cur.fetchone()
    cur.close()
    return render_template('dashboard/seats/edit.html', seat=seat)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_seat(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM seats WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Seat berhasil dihapus!', 'success')
    return redirect(url_for('seats.seats'))


@bp.route('/reserve/<int:id>', methods=['POST'])
def reserve_table(id):
    if 'logged_in' not in session or session['role'] != 'user':
        flash('Kamu tidak punya akses', 'danger')
        return redirect(url_for('seats.seats'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE seats SET status = 'reserved' WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Meja berhasil direservasi!', 'success')
    return redirect(url_for('menus.menus'))