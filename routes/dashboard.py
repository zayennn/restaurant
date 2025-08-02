from flask import Blueprint, render_template
from middlewares import login_required, role_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
@role_required('petugas', 'admin')
def dashboard():
    return render_template('dashboard/index.html')