"""
Demonstração do sistema de pedidos e cálculo de preços.
Usa dados de exemplo para testar fluxo completo.
"""

from legacy.clients import load_clients, register_client
from legacy.order_service import process_order
from legacy.price_calculator import calculate_final_price


def main():
    """Executa cenário de teste com cliente gold e lista de produtos."""
    # Carrega clientes do arquivo
    clients = load_clients("clientes.txt")
    print("Clientes carregados:", clients)

    # Testa registro de novo cliente
    new_client = {"name": "João Silva", "email": "joao@email.com", "tier": "gold"}
    register_client(new_client)

    # Processa pedido para cliente existente
    if clients:
        client = clients[0]
        process_order(client, 100.0)

    # Calcula preço final com múltiplos itens
    items = [
        {"name": "Produto A", "price": 50.0},
        {"name": "Produto B", "price": 30.0},
        {"name": "Produto C", "price": 20.0},
    ]
    final_price = calculate_final_price(items)
    print(f"Preço final calculado: R$ {final_price:.2f}")


if __name__ == "__main__":
    main()
