from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Silakan login dulu.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('Kamu tidak punya akses ke halaman ini.', 'danger')
                return redirect(url_for('seats.seats'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def guest_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            flash('Kamu sudah login!', 'danger')

            if session['role'] == 'admin' or session['role'] == 'petugas' :
                return redirect(url_for('dashboard.dashboard'))
            else :
                return redirect(url_for('seats.seats'))
        return f(*args, **kwargs)
    return decorated_function