from legacy.order_service import process_order
from legacy.clients import register_client

orders = [
    {"Client": "TransLog", "Product": "diesel", "Quantity": 1200, "Voucher": "MEGA10"},
    {"Client": "MoveMais", "Product": "gasolina", "Quantity": 300, "Voucher": None},
    {"Client": "EcoFrota", "Product": "etanol", "Quantity": 50, "Voucher": "NOVO5"},
    {"Client": "PetroPark", "Product": "lubrificante", "Quantity": 12, "Voucher": "LUB2"},
]

clients = [
    {"name": "Ana Paula", "email": "ana@@petrobahia", "cnpj": "123"},
    {"name": "Carlos", "email": "carlos@petrobahia.com", "cnpj": "456"},
]

print("==== Início processamento PetroBahia ====")

for client in clients:
    ok = register_client(client)
    if ok:
        print("Client ok: ", client["name"])
    else:
        print("Issues with client:", client)

order_value = []
for order in orders:
    value = process_order(order)
    order_value.append(value)
    print("Order:", order, "-- final cost: ", value)

print("TOTAL = ", sum(order_value))
print("==== Fim processamento PetroBahia ====")
