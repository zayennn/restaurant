from flask import Flask
from config import Config
from extensions import mysql, bcrypt
from routes import auth, dashboard, users, seats, menus, reservations, profile, cart

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
bcrypt.init_app(app)

# Register Blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(users.bp)
app.register_blueprint(seats.bp)
app.register_blueprint(menus.bp)
app.register_blueprint(reservations.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(cart.bp)

if __name__ == '__main__':
    app.run(debug=True)