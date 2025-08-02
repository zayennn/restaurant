from flask import Blueprint, render_template

bp = Blueprint('seats', __name__, url_prefix='/dashboard/seats')

@bp.route('/')
def seats():
    return render_template('dashboard/seats/index.html')
