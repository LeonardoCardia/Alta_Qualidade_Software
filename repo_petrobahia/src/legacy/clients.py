"""
Gerenciamento de dados de clientes.
Carrega e valida informações de clientes a partir de arquivos de texto.
"""

import re

REGEX_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def load_clients(file_path):
    """
    Carrega clientes do arquivo CSV com formato: nome,email,tier.
    Ignora linhas malformadas silenciosamente.
    """
    clients = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    client = {
                        "name": parts[0].strip(),
                        "email": parts[1].strip(),
                        "tier": parts[2].strip(),
                    }
                    clients.append(client)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Arquivo de clientes não encontrado: {file_path}"
        ) from exc

    return clients


class ClientValidator:
    """Valida campos obrigatórios e formato de email dos clientes."""

    @staticmethod
    def validate_email(email):
        """Verifica se email possui formato válido (user@domain.com)."""
        return bool(re.match(REGEX_EMAIL, email))

    def validate(self, client):
        """
        Verifica se cliente possui 'name' e 'email' válidos.
        Imprime erro no console caso falhe.
        """
        if "email" not in client or "name" not in client:
            print("Campos obrigatórios faltando")
            return False
        if not self.validate_email(client["email"]):
            print("Formato de email inválido")
            return False
        return True


class ClientRepository:
    """Persiste clientes em arquivo de texto no formato de dicionário Python."""

    def __init__(self, file_path="clients.txt"):
        """Define o caminho do arquivo de persistência."""
        self.file_path = file_path

    def save(self, client):
        """Adiciona cliente ao final do arquivo usando str(dict)."""
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(str(client) + "\n")

    def load_all(self):
        """Retorna todos os clientes do arquivo no formato CSV."""
        return load_clients(self.file_path)


class EmailService:
    """Simula envio de emails (apenas imprime no console)."""

    @staticmethod
    def send_greeting(email):
        """Envia email de boas-vindas simples."""
        print(f"Enviando email de saudação para {email}")

    def send_welcome(self, email, name):
        """Envia email de boas-vindas personalizado com nome do cliente."""
        print(f"Enviando email de boas-vindas para {name} em {email}")


def register_client(client):
    """
    Fluxo completo de registro: valida, salva e envia email de saudação.
    Retorna False se validação falhar.
    """
    validator = ClientValidator()
    repository = ClientRepository()
    email_service = EmailService()

    if not validator.validate(client):
        return False

    repository.save(client)
    email_service.send_greeting(client["email"])
    return True
