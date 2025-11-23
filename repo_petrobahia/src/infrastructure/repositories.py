from typing import List

from domain.entities import Client
from domain.repositories import ClientRepository as IClientRepository


class FileClientRepository(IClientRepository):
    """Repositório para persistir clientes em arquivos de texto."""

    def __init__(self, file_path: str):
        """Inicializa o repositório de clientes."""
        self._file_path = file_path

    def exists(self, email: str) -> bool:
        """Verifica se um cliente com o email já existe."""
        try:
            clients = self.load_all()
            return any(client.email == email for client in clients)
        except FileNotFoundError:
            return False

    def save(self, client: Client) -> None:
        """Salva o cliente no arquivo em formato CSV."""
        if self.exists(client.email):
            raise ValueError(f"Cliente com email {client.email} já está cadastrado")
        
        with open(self._file_path, "a", encoding="utf-8") as file:
            line = f"{client.name},{client.email},{client.tier}\n"
            file.write(line)

    def load_all(self) -> List[Client]:
        """Carrega todos os clientes do arquivo."""
        clients = []

        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(",")
                    if len(parts) == 3:
                        try:
                            client = Client(
                                name=parts[0].strip(),
                                email=parts[1].strip(),
                                tier=parts[2].strip(),
                            )
                            clients.append(client)
                        except ValueError:
                            # Pula clientes inválidos
                            continue

        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Arquivo de clientes não encontrado: {self._file_path}"
            ) from exc

        return clients
