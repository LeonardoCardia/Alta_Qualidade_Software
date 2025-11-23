import re

from domain.entities import Client
from domain.services import ClientValidator as IClientValidator


class EmailValidator:
    """Valida o formato de email seguindo os padrões RFC."""

    EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    def is_valid(self, email: str) -> bool:
        """Verifica se o email possui formato válido."""
        if not email:
            return False
        return bool(re.match(self.EMAIL_REGEX, email))


class ClientValidator(IClientValidator):
    """Valida dados do cliente usando composição."""

    def __init__(self, email_validator: EmailValidator):
        """Inicializa o validador de cliente."""
        self._email_validator = email_validator

    def validate(self, client: Client) -> bool:
        """Valida os dados do cliente."""
        if not client.name or not client.name.strip():
            raise ValueError("O nome do cliente não pode estar vazio")

        if not client.email or not client.email.strip():
            raise ValueError("O email do cliente não pode estar vazio")

        if not self._email_validator.is_valid(client.email):
            raise ValueError(f"Formato de email inválido: {client.email}")

        if not client.tier or not client.tier.strip():
            raise ValueError("O nível do cliente não pode estar vazio")

        return True
