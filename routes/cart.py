from flask import Blueprint, session, redirect, url_for, request, flash, render_template
from extensions import mysql
import MySQLdb.cursors

bp = Blueprint('cart', __name__, url_prefix='/dashboard/cart')

@bp.route('/')
def cart():
    cart_items = session.get('cart', [])
    reservation = session.get('reservation', None)
    return render_template('dashboard/cart/index.html', cart_items=cart_items, reservation=reservation)

@bp.route('/add/<int:menu_id>', methods=['POST'])
def add_to_cart(menu_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM menus WHERE id=%s", (menu_id,))
    menu = cur.fetchone()
    cur.close()

    if not menu:
        flash('Menu tidak ditemukan.', 'error')
        return redirect(url_for('menus.menus'))

    cart = session.get('cart', [])

    existing = next((item for item in cart if item['id'] == menu['id']), None)
    if existing:
        session['swal'] = {
            'title': 'Menu sudah ada di keranjang',
            'text': 'Silakan buka halaman keranjang untuk menambah jumlah menu.',
            'icon': 'info'
        }
        return redirect(url_for('menus.menus'))

    cart.append({
        'id': menu['id'],
        'name': menu['name'],
        'price': float(menu['price']),
        'qty': 1,
        'image': menu['image'],
        'category': menu['category']
    })

    session['cart'] = cart
    session['swal'] = {
        'title': 'Berhasil ditambahkan!',
        'text': f"{menu['name']} sudah masuk ke keranjang.",
        'icon': 'success'
    }

    return redirect(url_for('menus.menus'))

@bp.route('/remove/<int:menu_id>', methods=['POST'])
def remove_from_cart(menu_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != menu_id]
    session['cart'] = cart
    session.modified = True
    flash('Menu berhasil dihapus dari cart.', 'info')
    return redirect(url_for('cart.cart'))

@bp.route('/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    flash('Semua item dihapus dari cart.', 'info')
    return redirect(url_for('cart.cart'))


@bp.route('/update_qty', methods=['POST'])
def update_qty():
    data = request.json
    menu_id = data.get('id')
    qty = data.get('qty')

    if not menu_id or not qty:
        return {'success': False}, 400

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == menu_id:
            item['qty'] = qty
            break
    session['cart'] = cart
    session.modified = True
    return {'success': True}


# invoice
@bp.route('/invoice')
def invoice():
    cart_items = session.get('cart', [])
    reservation = session.get('reservation', None)

    subtotal = sum(item['price'] * item['qty'] for item in cart_items)
    tax = round(subtotal * 0.05)
    total = subtotal + tax

    return render_template(
        'dashboard/cart/payment/invoice.html',
        cart_items=cart_items,
        reservation=reservation,
        subtotal=subtotal,
        tax=tax,
        total=total
    )