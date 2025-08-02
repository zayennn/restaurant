from flask import Blueprint, render_template

bp = Blueprint('cart', __name__, url_prefix='/dashboard/cart')

@bp.route('/')
def cart():
    return render_template('dashboard/cart/index.html')
