# Python Webhook Sender

This example shows how to generate a signed webhook payload using Python.

The sender uses:

- RSA private key
- SHA-256 hashing
- PKCS#1 v1.5 padding
- Base64 encoded signature

## Requirements

Install the required package:

```text
pip install cryptography
```

## Example

```python
import json
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


data = {
    "event": "payment.completed",
    "id": 123
}


message = json.dumps(
    data,
    separators=(",", ":"),
    sort_keys=True
).encode("utf-8")


signature = private_key.sign(
    message,
    padding.PKCS1v15(),
    hashes.SHA256()
)


sign = base64.b64encode(
    signature
).decode("ascii")


payload = {
    "sign": sign,
    "data": data
}
```
 
## Send Webhook

Send the generated payload to:

```http
POST https://your-domain.com/api/v1/webhook
```

Example request:

```json
{
  "sign": "BASE64_SIGNATURE",
  "data": {
    "event": "payment.completed",
    "id": 123
  }
}
```

## Notes

The JSON serialization must be identical between sender and receiver.

The following configuration is used:

- Sorted keys
- Compact separators
- UTF-8 encoding

The receiver verifies the signature using the public key.