import hashlib
import string

ALPHABET = string.ascii_letters  # a-zA-Z


def generate_id_from_base(base_id: str, length: int = 10) -> str:
    """
    Генерирует ID из букв на основе базового ID
    Одинаковый base_id всегда дает одинаковый результат
    """
    digest = hashlib.sha256(str(base_id).encode()).digest()

    return "".join(ALPHABET[b % len(ALPHABET)] for b in digest[:length])
