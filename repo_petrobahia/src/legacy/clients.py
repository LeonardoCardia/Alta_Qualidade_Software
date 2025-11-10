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
