import sys
from DTO import Hat, Supplier, Order
import atexit
from Repository import Repository


def parse_input(file, repo):
    with open(file) as config:
        lines = config.readlines()
        hat_type_amount = int(lines[0].split(',')[0])
        supplier_amount = int(lines[0].split(',')[1])

        for i in range(1, hat_type_amount + 1):
            current_line = lines[i].replace("\n", "")
            hat_info = current_line.split(",")
            hat_id = int(hat_info[0])
            hat_topping = hat_info[1]
            supplier = int(hat_info[2])
            quantity = int(hat_info[3])
            hat_to_add = Hat(hat_id, hat_topping, supplier, quantity)
            repo.hats.insert(hat_to_add)

        for i in range(1 + hat_type_amount, 1 + hat_type_amount + supplier_amount):
            current_line = lines[i].replace("\n", "")
            supplier_info = current_line.split(",")
            supplier_id = int(supplier_info[0])
            supplier_name = supplier_info[1]
            supplier_to_add = Supplier(supplier_id, supplier_name)
            repo.suppliers.insert(supplier_to_add)


if __name__ == '__main__':
    config = sys.argv[1]
    orders = sys.argv[2]
    # config = "example_input/config.txt"
    # orders = "example_input/orders.txt"
    # output = "output.txt"
    output = sys.argv[3]

    repo = Repository(sys.argv[4])
    atexit.register(repo.close)
    repo.create_tables()

    parse_input(config, repo)
    order_counter = 1
    with open(orders) as orders, open(output, "w") as output:
        lines = orders.readlines()
        for line in lines:
            current_line = line.replace('\n', "")
            order_info = current_line.split(",")
            location = order_info[0]
            topping = order_info[1]
            order_hat_id, order_hat_quant, order_supplier = repo.hats.find(topping)
            order_id = repo.orders.get_id_counter() + 1
            current_order = Order(order_id, location, order_hat_id)
            if order_hat_quant == 1:
                repo.hats.remove(order_hat_id)
            else:
                repo.hats.update_quantity(order_hat_id)

            repo.orders.insert(current_order)
            order_supplier = repo.suppliers.find_name(order_supplier)
            output.write(topping+","+order_supplier+","+location+"\n")

