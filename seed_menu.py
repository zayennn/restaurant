import random
from faker import Faker
import MySQLdb

# Setup Faker
faker = Faker()

# Koneksi ke MySQL
db = MySQLdb.connect(
    host="localhost",
    user="root",
    password="",
    database="db_restaurant_flask",
    charset='utf8mb4'
)

cursor = db.cursor()

categories = ['Appetizers', 'Main Course', 'Desserts', 'Drinks']

# Seeder logic
for i in range(50):
    name = faker.word().capitalize() + " " + faker.word().capitalize()
    description = faker.sentence(nb_words=8)
    price = random.randint(10000, 100000)
    category = random.choice(categories)
    qty = random.randint(1, 50)
    image = ''

    sql = """
    INSERT INTO menus (name, description, price, category, qty, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, description, price, category, qty, image)
    cursor.execute(sql, values)

db.commit()
cursor.close()
db.close()

print("✅ 50 menu berhasil di-seed.")