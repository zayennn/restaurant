from flask import Blueprint, render_template

bp = Blueprint('menus', __name__, url_prefix='/dashboard/menus')

@bp.route('/')
def menus():
    return render_template('dashboard/menus/index.html')