import fcntl

from DTO import Hat, Supplier, Order


class Hats:
    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, hat):
        self._conn.execute("""
                INSERT INTO hats(id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
            """, [hat.id, hat.topping, hat.supplier, hat.quantity])

    # def find(self, hat_topping):
    #     c = self._conn.cursor()
    #     c.execute("""
    #         SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?
    #     """, [hat_topping])
    #     return Hat(*c.fetchone())

    def find(self, hat_topping):
        self.c.execute("""
               SELECT id, quantity, supplier FROM hats WHERE topping = ? ORDER BY supplier ASC
           """, (hat_topping,))
        output = self.c.fetchone()
        return output[0], output[1], output[2]

    def remove(self, hat_id):
        self.c.execute("""
            DELETE FROM hats
            WHERE id = ({})
            """.format(hat_id))

    def update_quantity(self, hat_id):
        updated_quant = self.find_quantity(hat_id) - 1
        self.c.execute("""
                UPDATE hats
                SET quantity = ? WHERE id = ?
                """, [updated_quant, hat_id])

    def find_quantity(self, hat_id):
        self.c.execute("""
            SELECT quantity FROM hats WHERE id= ?
        """, [hat_id])
        return int(*self.c.fetchone())

    def get_supplier_id(self, hat_id):
        self.c.execute(""""
            SELECT supplier FROM hats WHERE id=? 
        """, [hat_id])
        return self.c.fetchone()[0]


class Suppliers:

    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers(id, name) VALUES (?, ?)
            """, [supplier.id, supplier.name])

    def find_name(self, supplier_id):
        self.c.execute("""
            SELECT name FROM suppliers WHERE id = ?
        """, [supplier_id])
        return self.c.fetchone()[0]


class Orders:
    def __init__(self, conn):
        self._conn = conn
        self.c = self._conn.cursor()

    def insert(self, order):
        self._conn.execute("""
                INSERT INTO orders(id, location, hat) VALUES (?, ?, ?)
            """, [order.id, order.location, order.hat])

    def get_id_counter(self):
        self.c.execute("""
            SELECT MAX(id) FROM orders 
            """)
        count = self.c.fetchone()[0]
        if count is None:
            return 0
        return count
