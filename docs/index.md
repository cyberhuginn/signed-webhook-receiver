# Signed Webhook Receiver

> Verify. Trust. Process.

A lightweight and secure webhook receiver built with **FastAPI** that verifies incoming webhook requests using **RSA SHA-256 digital signatures**.

## Overview

Signed Webhook Receiver is a secure webhook gateway that validates incoming requests before processing them.

The receiver never trusts incoming messages unless the provided signature can be verified using the configured RSA public key.

## How It Works

```text
Sender
  |
  | Create webhook payload
  |
  | Sign data with RSA private key
  |
  v
Webhook Receiver
  |
  | Verify signature with RSA public key
  |
  +-- Valid signature ---> Process data
  |
  +-- Invalid signature -> Reject request
```
## Features
- RSA SHA-256 signature verification 
- RSA PKCS#1 v1.5 signing support
- FastAPI + Uvicorn
- Docker ready
- Traefik compatible
- Public key based verification
- Lightweight microservice architecture

## Request Flow
The sender creates a payload containing:

- data — webhook event information
- sign — Base64 encoded RSA signature

### Example:
```json
{
  "sign": "BASE64_SIGNATURE",
  "data": {
      "event": "payment.completed",
      "id": 123
  }
}
```

## Supported Languages

Webhook senders can be implemented using:

- Python
- JavaScript / Node.js
- Go

[//]: # (- Java)
[//]: # (- Rust)
[//]: # (- C)
[//]: # (- C++)

Each implementation must follow the same signing protocol to generate compatible signatures.

## Security Model

This project uses asymmetric cryptography:

- The sender owns the private key
- The receiver only stores the public key
- Incoming requests are accepted only after signature verification

The private key must never be shared with the receiver.

## Production Recommendations

For production environments:

- Always use HTTPS
- Protect your private keys
- Add timestamps to prevent replay attacks
- Validate webhook payloads before processing
- Use canonical JSON before signing

### Sender Examples

- [Python](examples/python.md)
- [JavaScript](examples/javascript.md)
- [Go](examples/go.md)

[//]: # (- [Java]&#40;examples/java.md&#41;)
[//]: # (- [Rust]&#40;examples/rust.md&#41;)
[//]: # (- [C]&#40;examples/c.md&#41;)
[//]: # (- [C++]&#40;examples/cpp.md&#41;)

## API

Webhook endpoint:

```http
POST /api/v1/webhook
```

Request body:

```json
{
  "sign": "BASE64_SIGNATURE",
  "data": {
    "event": "payment.completed",
    "id": 123
  }
}
```

Successful response:

```json
{
  "status": "ok"
}
```

Invalid signatures are rejected.

## License

MIT