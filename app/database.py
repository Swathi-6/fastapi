import sqlite3
from typing import Any, List

from schema.models import CreateProduct, ReadProduct, UpdateProduct

class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect("productsdb.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        self.cur.execute(""" 
                         CREATE TABLE IF NOT EXISTS PRODUCTS(
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL UNIQUE,
                         price REAL NOT NULL,
                         stock INTEGER NOT NULL)
                         """)
        
    def create(self, data: CreateProduct):
        self.cur.execute(""" INSERT INTO PRODUCTS(name, price, stock)
                         VALUES (:name, :price, :stock) """,
                         data.model_dump())
        self.cur.execute("SELECT MAX(id) FROM products")
        self.conn.commit()
        id = self.cur.lastrowid
        print("created id: ", id)
        return id
    
    def get(self, id:int) -> dict[str, Any] | None:
        self.cur.execute("SELECT * FROM products WHERE id = :id",{'id':id})
        row = self.cur.fetchone()
        if row:
            return {'id': row[0], 'name':row[1], 'price':row[2], 'stock':row[3]}
        return None
    
    def get_all(self) -> List[ReadProduct]:
        self.cur.execute("SELECT * FROM products")
        rows = self.cur.fetchall()
        return rows
    
    def update(self, id:int, data:UpdateProduct) -> dict[str, Any] | None:
        new_data = data.model_dump(exclude_none=True)
        clause = ",".join(f"{key}=:{key}" for key in new_data)
        self.cur.execute(""" UPDATE products
                         SET """ + clause + """ WHERE id = :id""", {'id':id, **new_data})
        self.conn.commit()
        return self.get(id)
    
    def delete(self, id:int):
        self.cur.execute("DELETE FROM products WHERE id = :id",{'id':id})
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
# db = Database()
# result = db.get_all()
# print("Before: ",result)

# up = db.update(1, UpdateProduct.model_validate({"name":"Mug"}))
# print(up)

# result = db.get_all()
# print("After: ",result)