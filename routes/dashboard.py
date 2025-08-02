from flask import Blueprint, render_template

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def dashboard():
    return render_template('dashboard/index.html')