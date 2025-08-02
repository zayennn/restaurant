from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import mysql
import MySQLdb.cursors
from datetime import datetime

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

    date = request.form.get('reservation_date')
    time = request.form.get('reservation_time')

    # fallback waktu jika tidak tersedia
    if session['role'] in ['admin', 'petugas'] or not date or not time:
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H:%M:%S')

    user_id = session.get('user_id')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM seats WHERE id = %s", (id,))
    seat = cur.fetchone()

    if not seat:
        flash("Meja tidak ditemukan.", "danger")
        return redirect(url_for('seats.seats'))

    cur.execute("""
        UPDATE seats 
        SET status = 'reserved', reservation_date = %s, reservation_time = %s, reserved_by = %s
        WHERE id = %s
    """, (date, time, user_id, id))
    mysql.connection.commit()
    cur.close()

    session['reservation'] = {
        'id': seat['id'],
        'name': seat['name'],
        'capacity': seat['capacity'],
        'date': str(date),
        'time': str(time)
    }

    flash(f'Meja {seat["name"]} berhasil direservasi!', 'success')
    return redirect(url_for('menus.menus'))

@bp.route('/cancel-reservation', methods=['POST'])
def cancel_reservation():
    if 'logged_in' not in session or session['role'] != 'user':
        flash('Kamu tidak punya akses', 'danger')
        return redirect(url_for('seats.seats'))

    reservation = session.get('reservation')
    if reservation:
        seat_id = reservation.get('id')

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE seats 
            SET status = 'available', reserved_by = NULL, reservation_date = NULL, reservation_time = NULL 
            WHERE id = %s
        """, (seat_id,))
        mysql.connection.commit()
        cur.close()

        session.pop('reservation', None)
        flash('Reservasi berhasil dibatalkan.', 'success')
    else:
        flash('Kamu belum melakukan reservasi.', 'warning')

    return redirect(url_for('seats.seats'))