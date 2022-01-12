import sqlite3
from DAO import Hats, Suppliers, Orders
from DTO import Order


def check_validity(hat):
    if hat.quantity == 0:
        Hats.remove(hat.id)


class Repository:
    def __init__(self, db_file):
        self._conn = sqlite3.connect(db_file)
        self.hats = Hats(self._conn)
        self.suppliers = Suppliers(self._conn)
        self.orders = Orders(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
            id              INTEGER     PRIMARY KEY,
            topping         TEXT        NOT NULL,
            supplier        INTEGER     NOT NULL,
            quantity        INTEGER     NOT NULL
        );
        
        CREATE TABLE suppliers (
            id          INTEGER     PRIMARY KEY,
            name        TEXT        NOT NULL    
        );
        
        CREATE TABLE orders (
            id          INTEGER     PRIMARY KEY,
            location    TEXT        NOT NULL,
            hat         INTEGER     REFERENCES hats(id)
        );
    """)

    # def take_order(self, order_counter, _location, _hat):
    #     Orders.insert(Order(order_counter, _location, _hat))
    #     search = Hats.find(_hat)
    #     Hats.update_quantity(search.id, search.quantity - 1)
    #     check_validity(search)
    #     return search.topping, search.supplier, _location



