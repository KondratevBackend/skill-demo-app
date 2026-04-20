import random
import secrets
import string

ALPHABET = string.ascii_uppercase + string.digits
BRAND = "skill-demo-app"


def generate_coupon_code():
    word = random.choice(["LOVE", "FAST", "SECURE"])
    random_suffix = "".join(secrets.choice(ALPHABET) for _ in range(4))
    return f"{word}-{BRAND}-{random_suffix}"
