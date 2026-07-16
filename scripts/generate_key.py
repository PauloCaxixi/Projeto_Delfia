from cryptography.fernet import Fernet


def generate_key() -> str:
    """Gera uma chave segura compatível com Fernet."""

    return Fernet.generate_key().decode("utf-8")


if __name__ == "__main__":
    print(generate_key())