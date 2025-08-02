from flask import Blueprint, render_template

bp = Blueprint('reservations', __name__, url_prefix='/dashboard/reservations')

@bp.route('/')
def reservations():
    return render_template('dashboard/reservations/index.html')
