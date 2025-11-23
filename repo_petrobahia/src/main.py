from domain.entities import Client, OrderItem
from infrastructure.repositories import FileClientRepository
from services.discount import QuantityDiscountCalculator, TierDiscountCalculator
from services.email import ConsoleEmailService
from services.tax import TaxCalculator
from services.validation import ClientValidator, EmailValidator
from use_cases.client_management import RegisterClientUseCase
from use_cases.order_processing import GenerateOrderSummaryUseCase, ProcessOrderUseCase
from use_cases.price_calculation import CalculateFinalPriceUseCase


def main():
    """Executa cenários de demonstração com a arquitetura refatorada."""
    print("=== Sistema de Gerenciamento de Pedidos PetroBahia ===\n")

    # Inicializa infraestrutura e serviços
    client_repository = FileClientRepository("clientes.txt")
    email_validator = EmailValidator()
    client_validator = ClientValidator(email_validator)
    email_service = ConsoleEmailService()
    discount_calculator = TierDiscountCalculator()
    quantity_discount = QuantityDiscountCalculator()
    tax_calculator = TaxCalculator(tax_rate=0.10)

    # Inicializa casos de uso
    register_client_use_case = RegisterClientUseCase(
        repository=client_repository,
        validator=client_validator,
        email_sender=email_service,
    )
    process_order_use_case = ProcessOrderUseCase(
        discount_calculator=discount_calculator
    )
    generate_summary_use_case = GenerateOrderSummaryUseCase()
    calculate_price_use_case = CalculateFinalPriceUseCase(
        quantity_discount=quantity_discount,
        tax_calculator=tax_calculator,
    )

    # Cenário 1: Carregar clientes existentes
    print("1. Carregando clientes existentes do arquivo...")
    try:
        clients = client_repository.load_all()
        print(f"   Carregados {len(clients)} cliente(s):")
        for client in clients:
            print(f"   - {client.name} ({client.email}) - Nível: {client.tier}")
    except FileNotFoundError:
        print("   Nenhum cliente existente encontrado.")
        clients = []
    print()

    # Cenário 2: Registrar novos clientes
    print("2. Registrando novos clientes...")
    novos_clientes = [
        Client(name="João Silva", email="joao@email.com", tier="gold"),
        Client(name="Maria Santos", email="maria@email.com", tier="silver"),
        Client(name="Pedro Costa", email="pedro@email.com", tier="bronze"),
        Client(name="Fernanda Lima", email="fernanda@email.com", tier="gold"),
    ]
    
    for new_client in novos_clientes:
        try:
            register_client_use_case.execute(new_client)
            print(f"Cliente {new_client.name} registrado com sucesso!")
        except ValueError as e:
            print(f"Falha no registro de {new_client.name}: {e}")
    print()

    # Cenário 3: Processar pedido para cliente existente
    if clients:
        print("3. Processando pedido para o primeiro cliente...")
        client = clients[0]
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]

        try:
            order = process_order_use_case.execute(client, items)
            summary = generate_summary_use_case.execute(order)
            print(summary)
        except ValueError as e:
            print(f"   Falha no processamento do pedido: {e}")
        print()

    # Cenário 4: Calcular preço final com descontos por quantidade e impostos
    print("4. Calculando preço final com descontos por quantidade e impostos...")
    items = [
        OrderItem(name="Produto A", price=50.0),
        OrderItem(name="Produto B", price=30.0),
        OrderItem(name="Produto C", price=20.0),
    ]

    try:
        final_price = calculate_price_use_case.execute(items)
        print(f"   Itens: {len(items)}")
        print(f"   Subtotal: R$ {sum(item.price for item in items):.2f}")
        print(f"   Preço final (com desconto e imposto): R$ {final_price:.2f}")
    except ValueError as e:
        print(f"   Falha no cálculo: {e}")
    print()

    print("=== Demonstração concluída ===")


if __name__ == "__main__":
    main()
