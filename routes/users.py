from flask import Blueprint, render_template

bp = Blueprint('users', __name__, url_prefix='/dashboard/users')

@bp.route('/')
def users():
    return render_template('dashboard/users/index.html')