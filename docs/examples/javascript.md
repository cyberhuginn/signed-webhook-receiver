# JavaScript Webhook Sender

This example shows how to generate a signed webhook payload using **Node.js**.

> The private key must only exist on the backend/server side.  
> Never expose the RSA private key in browser JavaScript.

The sender uses:

- Node.js built-in `crypto` module
- RSA SHA-256
- PKCS#1 v1.5 padding
- Base64 encoded signature

## Requirements

Node.js 18+

## Example

```javascript
import crypto from "node:crypto";
import fs from "node:fs";


const privateKey = fs.readFileSync(
    "private.pem"
);


const data = {
    event: "payment.completed",
    id: 123
};


const message = JSON.stringify(
    {
        event: data.event,
        id: data.id
    }
);


const signature = crypto.sign(
    "RSA-SHA256",
    Buffer.from(message, "utf-8"),
    {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_PADDING
    }
);


const sign = signature.toString(
    "base64"
);


const payload = {
    sign,
    data
};


console.log(payload);
```
## Send Webhook
Send the generated payload to:
```http request
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
The receiver verifies the signature using the RSA public key.
The data used for signing must match the receiver’s canonical JSON format.

## The signing process
```text
Data
 |
 v
Canonical JSON
 |
 v
UTF-8 bytes
 |
 v
RSA SHA-256
 |
 v
Base64 signature
```