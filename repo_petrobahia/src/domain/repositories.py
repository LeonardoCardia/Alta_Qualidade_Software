from abc import ABC, abstractmethod
from typing import List

from domain.entities import Client


class ClientReader(ABC):
    """Interface para leitura de dados de clientes."""

    @abstractmethod
    def load_all(self) -> List[Client]:
        """Carrega todos os clientes do armazenamento."""
        ...

    @abstractmethod
    def exists(self, email: str) -> bool:
        """Verifica se um cliente com o email já existe."""
        ...


class ClientWriter(ABC):
    """Interface para escrita de dados de clientes."""

    @abstractmethod
    def save(self, client: Client) -> None:
        """Salva um cliente no armazenamento."""
        ...


class ClientRepository(ClientReader, ClientWriter):
    """Interface completa de repositório de clientes."""

    ...
