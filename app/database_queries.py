import sqlite3

connection = sqlite3.connect("productsdb.db")
cursor = connection.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS PRODUCTS(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL UNIQUE,
                   price REAL NOT NULL,
                   stock INTEGER NOT NULL,
                   status TEXT NOT NULL
               )
''')

# INSERT
# cursor.execute('''
#                INSERT INTO PRODUCTS(name, price, stock, status) 
#                VALUES ("Laptop", 2000, 7, "In Stock"),
#                ("Mouse", 10, 20, "In Stock"),
#                ("Bottle", 10, 10, "In Stock"),
#                ("Pen", 1, 10, "In Stock"),
#                ("Phone", 1000, 10, "In Stock");
#                ''')


# cursor.execute('SELECT * FROM PRODUCTS WHERE stock > 5;')
# # row = cursor.fetchone()
# # print(row)
# # print("="*40)
# rows = cursor.fetchmany(3)
# print("Products with stock units > 5")
# print(rows)

# UPDATE
# cursor.execute(""" 
#                UPDATE products 
#                SET status = "Low Stock"
#                WHERE stock < 10;
#                """)
# rows = cursor.rowcount
# print(rows)

# DELETE
# cursor.execute("DELETE FROM products where name='Mouse'")

# GET ALL
cursor.execute('SELECT * FROM PRODUCTS')
rows = cursor.fetchall()
print(rows)

# input_id = input("Enter ID: ") 3 OR 1=1 exposed all rows
# cursor.execute(f"SELECT * FROM PRODUCTS WHERE ID={input_id}")
# rows = cursor.fetchall()
# print(rows)

input_id = input("Enter ID: ")
cursor.execute("SELECT * FROM PRODUCTS WHERE ID=?", (input_id))
rows = cursor.fetchall()
print(rows)


connection.commit()
connection.close()