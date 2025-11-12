"""
Module for client data management.

This module provides functionality to load and manage client information
from text files.
"""


def load_clients(file_path):
    """
    Load client data from a text file.

    Args:
        file_path (str): Path to the file containing client data.

    Returns:
        list: A list of dictionaries containing client information.
              Each dictionary has 'name', 'email', and 'tier' keys.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    clients = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    client = {
                        'name': parts[0].strip(),
                        'email': parts[1].strip(),
                        'tier': parts[2].strip()
                    }
                    clients.append(client)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Client file not found: {file_path}"
        ) from exc
    
    return clients


import re

REGEX_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class ClientValidator:
    def validate(self, client):
        if "email" not in client or "name" not in client:
            print("Missing mandatory fields")
            return False
        if not re.match(REGEX_EMAIL, client["email"]):
            print("Invalid email format")
            return False
        return True


class ClientRepository:
    def save(self, client):
        file = open("clients.txt", "a", encoding="utf-8")
        file.write(str(client) + "\n")
        file.close()


class EmailService:
    def send_greeting(self, email):
        print("Sending greeting email to ", email)


def register_client(client):
    validator = ClientValidator()
    repository = ClientRepository()
    email_service = EmailService()
    
    if not validator.validate(client):
        return False
    
    repository.save(client)
    email_service.send_greeting(client["email"])
    return True
