import json
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

PUBLIC_KEY_PATH = "keys/public.pem"

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = load_pem_public_key(
        f.read()
    )


def verify_signature(data: dict, signature: str):
    try:
        message = json.dumps(
            data,
            separators=(",", ":"),
            sort_keys=True
        ).encode()

        signature_bytes = base64.b64decode(signature)

        PUBLIC_KEY.verify(
            signature_bytes,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return True

    except Exception:
        return False
