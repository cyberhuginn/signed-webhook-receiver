# Signed Webhook Receiver

> Verify. Trust. Process.

<p align="center">
  <img src="./imgs/banner.png" alt="Signed Webhook Receiver Banner">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/cyberhuginn/signed-webhook-receiver?style=flat-square" />
  <img src="https://img.shields.io/github/stars/cyberhuginn/signed-webhook-receiver?style=flat-square" />
  <img src="https://img.shields.io/github/forks/cyberhuginn/signed-webhook-receiver?style=flat-square" />
  <img src="https://img.shields.io/github/issues/cyberhuginn/signed-webhook-receiver?style=flat-square" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker" />
  <img src="https://img.shields.io/badge/security-RSA%20signature-red?style=flat-square&logo=letsencrypt" />
</p>

A lightweight and secure webhook gateway for verifying RSA-signed requests.

---

## فارسی

> **اعتبارسنجی کن. اعتماد کن. پردازش کن.**

### معرفی

**Signed Webhook Receiver** یک سرویس سبک، مینیمال و امن برای دریافت و اعتبارسنجی درخواست‌های Webhook است که با **FastAPI** ساخته شده است.

این سرویس قبل از اینکه یک درخواست ورودی را بپذیرد یا داده‌های آن را در اختیار برنامه قرار دهد، امضای دیجیتال آن را با استفاده از **کلید عمومی RSA** بررسی می‌کند.

به زبان ساده، سرویس هیچ درخواستی را معتبر فرض نمی‌کند؛ مگر اینکه بتواند ثابت کند درخواست با **کلید خصوصیِ یک فرستنده مورد اعتماد** امضا شده است.

مستندات کامل پروژه:

[مشاهده مستندات](https://cyberhuginn.github.io/signed-webhook-receiver/)

---

## داستان شکل‌گیری پروژه

این پروژه از یک ایده‌ی تئوری یا صرفاً یک تمرین امنیتی شروع نشد؛ از یک مشکل واقعی در یک پروژه شروع شد.

در یکی از پروژه‌هایی که روی آن کار می‌کردم، سرور اصلی داخل ایران قرار داشت و امکان ارتباط مستقیم و قابل اتکا با **Telegram API** وجود نداشت.

در طرف دیگر، یک سرور خارجی داشتیم که می‌توانست به سرویس‌های خارجی دسترسی داشته باشد.

راه‌حل اولیه ساده بود:

```text
Server in Iran
      |
      | Request
      v
External Server
      |
      v
Telegram API
```

اما قرار نبود یک Proxy ساده ساخته شود.

موضوع مهم‌تر، **امنیت ارتباط بین دو سرور** بود.

درخواست‌هایی که از سرور اصلی ارسال می‌شدند ممکن بود حاوی اطلاعات مهمی باشند. بنابراین لازم بود سرور مقصد بتواند تشخیص دهد که:

* درخواست واقعاً از یک سرور مورد اعتماد آمده است.
* محتوای درخواست در مسیر تغییر نکرده است.
* یک شخص یا سرویس ناشناس نتواند به‌سادگی درخواست جعلی ارسال کند.

از همین نیاز، ایده‌ی **Signed Webhook Receiver** شکل گرفت.

---

## ایده اصلی

ساختار کلی سیستم به این شکل است:

```text
Source Server
     |
     | Signed Request
     |
     v
+----------------------+
| Signed Webhook       |
| Receiver             |
+----------------------+
     |
     | Verify Signature
     |
     +---- Invalid ----> Reject
     |
     |
     +---- Valid ------> Process
```

سرور مبدا داده را با **کلید خصوصی RSA** امضا می‌کند.

سرور مقصد کلید خصوصی را در اختیار ندارد و فقط **کلید عمومی** را نگه می‌دارد.

وقتی درخواست دریافت می‌شود، امضای آن با کلید عمومی بررسی می‌شود.

اگر امضا معتبر باشد، درخواست قابل اعتماد در نظر گرفته شده و پردازش می‌شود.

اگر امضا معتبر نباشد، درخواست رد می‌شود.

---

## چرا این پروژه ساخته شد؟

فرض کنید دو سرور دارید:

```text
┌──────────────────┐
│   Server A       │
│                  │
│   Private Key    │
└────────┬─────────┘
         │
         │ Signed Request
         ▼
┌──────────────────┐
│   Server B       │
│                  │
│   Public Key     │
└──────────────────┘
```

Server A درخواست را با کلید خصوصی امضا می‌کند.

Server B با کلید عمومی بررسی می‌کند که:

1. درخواست توسط فرستنده مورد اعتماد امضا شده است.
2. محتوای درخواست بعد از امضا تغییر نکرده است.
3. درخواست توسط یک فرستنده ناشناس جعل نشده است.

این مدل برای ارتباطات **Server-to-Server**، Webhookها، APIهای داخلی، Event Notificationها و سرویس‌های توزیع‌شده کاربرد زیادی دارد.

---

## یک سناریوی واقعی

یکی از کاربردهای اصلی این پروژه، انتقال درخواست از یک سرور با دسترسی محدود به یک سرور خارجی است.

برای مثال:

```text
┌─────────────────────┐
│ Server داخل ایران   │
│                     │
│ Application         │
└──────────┬──────────┘
           │
           │ Sign Request
           ▼
      Internet
           │
           ▼
┌─────────────────────┐
│ External Server     │
│                     │
│ Signed Receiver     │
└──────────┬──────────┘
           │
           ▼
      Telegram API
```

در این معماری، سرور اصلی مستقیماً با سرویس خارجی ارتباط برقرار نمی‌کند.

در عوض، درخواست موردنظر را برای سرور واسط ارسال می‌کند و سرور واسط پس از اعتبارسنجی درخواست، عملیات موردنظر را انجام می‌دهد.

این عملیات می‌تواند شامل موارد مختلفی باشد:

* ارسال درخواست به Telegram API
* Forward کردن درخواست به یک سرویس خارجی
* پردازش داده
* ذخیره اطلاعات
* اجرای یک Job
* اجرای یک Workflow
* فراخوانی یک API دیگر

---

## نکته مهم درباره امنیت

هدف این پروژه این نیست که جایگزین VPN، Network Tunnel یا Proxyهای تخصصی شود.

این سرویس یک مسئله مشخص را حل می‌کند:

> **اعتبارسنجی و انتقال امن درخواست‌های Application-Level بین دو سرور.**

در واقع تمرکز پروژه روی **Authentication، Integrity و Trust در سطح Application** است.

---

# English

## Overview

Signed Webhook Receiver is a lightweight and secure webhook service built with **FastAPI**.

It validates incoming webhook payloads using RSA digital signatures before accepting and processing them.

The receiver never trusts an incoming request unless its signature can be verified using the configured public key.

Documentation:

[See Documentation](https://cyberhuginn.github.io/signed-webhook-receiver/)

---

## When Should You Use This?

This project is useful when one server needs to securely send requests to another server and you want to make sure that:

* The message cannot be modified in transit.
* Only authorized servers can generate valid requests.
* Attackers cannot easily forge requests.
* The receiver can verify the authenticity and integrity of incoming data.

The sender signs the message using its **private RSA key**.

The receiving server verifies the signature using the corresponding **public key**.

This provides both **message integrity** and **sender authentication** without requiring the receiver to expose traditional credentials such as passwords or API keys.

---

## Example Architecture

```text
Server A                         Server B
────────                         ────────

Private Key                      Public Key
     │                                │
     │                                │
     ▼                                ▼
Sign Message  ────────────────>  Verify Signature
                                      │
                                      ▼
                                Process Request
```

Server B can verify that:

1. The request was signed by a trusted sender.
2. The request was not modified after signing.
3. The request was not generated by an unauthorized party.

---

## Features

* RSA SHA-256 signature verification
* Secure webhook endpoint
* FastAPI + Uvicorn
* Docker ready
* Traefik compatible
* Public-key based verification
* Lightweight microservice architecture

---

## Request Flow

```text
Client
  |
  | signed payload
  |
  v
Webhook Receiver
  |
  | RSA signature verification
  |
  +-- Valid signature ---> Process data
  |
  +-- Invalid signature -> Reject request
```

---

## Tech Stack

* Python 3.12
* FastAPI
* Uvicorn
* Cryptography
* Docker
* Traefik

---

## API

### Endpoint

```http
POST /api/v1/webhook
```

### Request Body

```json
{
  "sign": "BASE64_SIGNATURE",
  "data": {
    "event": "payment.completed",
    "id": 123
  }
}
```

### Response

#### Successful verification

```json
{
  "status": "ok"
}
```

#### Invalid signature

```http
HTTP/1.1 404 Not Found
```

---

## Documentation

Read the complete documentation:

[See Documentation](https://cyberhuginn.github.io/signed-webhook-receiver/)

---

## RSA Keys

Generate a private key:

```bash
openssl genrsa -out private.pem 2048
```

Generate the corresponding public key:

```bash
openssl rsa \
  -in private.pem \
  -pubout \
  -out public.pem
```

Only the **public key** is required by this service.

The **private key must remain on the sender side** and should never be deployed to the receiver.

---

## Security Notes

### Keep the private key private

The receiver should never have access to the sender's private key.

Only the public key should be configured on the receiving side.

### Canonicalize payloads

The exact same representation of the payload must be used when generating and verifying the signature.

For example, JSON serialization should use a deterministic format.

### Prevent replay attacks

Consider adding a timestamp, nonce, or unique request ID to the signed payload.

The receiver can then reject requests that are too old or have already been processed.

### Use HTTPS

RSA signatures protect the authenticity and integrity of the signed data, but production deployments should still use HTTPS.

---

## Docker

### Build

```bash
docker build -t signed-webhook-receiver .
```

### Run

```bash
docker run -p 8000:8000 signed-webhook-receiver
```

---

## Configuration

Before starting the service, configure your domain in the `.env` file.

Create a `.env` file:

```env
WEBHOOK_DOMAIN=hook.example.com
```

Replace `hook.example.com` with your own domain.

---

## Traefik Network

This project expects an existing Docker network named `proxy`.

Create the network before starting the container:

```bash
docker network create proxy
```

Your Traefik instance and the Signed Webhook Receiver must be connected to the same Docker network.

---

## Webhook Sender Example

The sender signs the payload using its private RSA key.

The receiver only needs the corresponding public key to verify the signature.

Example:

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
).encode()


signature = private_key.sign(
    message,
    padding.PKCS1v15(),
    hashes.SHA256()
)


sign = base64.b64encode(signature).decode()


payload = {
    "sign": sign,
    "data": data
}
```

Send the generated payload to:

```http
POST https://your-domain.com/api/v1/webhook
```

The receiver verifies the RSA signature before processing the data.

---

## Project Background

Signed Webhook Receiver started as a practical solution to a real infrastructure problem.

The original use case involved a server located in Iran that needed to communicate with external services such as Telegram API.

Instead of exposing credentials or relying on a simple proxy, the idea was to create a small application-level gateway where requests could be cryptographically signed by the source server and verified by the destination server.

The project was later extracted into an independent open-source microservice so that the same approach could be reused in other environments.

---

## What This Project Is — and Isn't

### It is:

* A secure webhook receiver
* An RSA signature verification service
* An application-level trust layer
* A lightweight server-to-server communication gateway
* A useful building block for distributed systems

### It is not:

* A VPN
* A network tunnel
* A general-purpose proxy
* A replacement for TLS
* A complete message queue

---

## License

MIT

---

## فارسی — خلاصه پروژه

**Signed Webhook Receiver** یک Gateway سبک و امن برای دریافت درخواست‌های Webhook و بررسی صحت آن‌ها با استفاده از امضای دیجیتال RSA است.

ایده اصلی ساده است:

**سرور فرستنده با کلید خصوصی درخواست را امضا می‌کند و سرور گیرنده با کلید عمومی صحت آن را بررسی می‌کند.**

به این ترتیب، سرور مقصد می‌تواند قبل از پردازش درخواست مطمئن شود که درخواست از یک فرستنده مورد اعتماد آمده و محتوای آن بعد از امضا تغییر نکرده است.

این پروژه برای سناریوهایی مثل موارد زیر مناسب است:

* ارتباط امن بین دو سرور
* Webhookهای حساس
* APIهای داخلی
* انتقال درخواست بین سرورهای داخل و خارج
* Event Notification
* سرویس‌های Microservice
* اجرای Job و Workflow از راه دور
* ارسال درخواست به سرویس‌های خارجی

این پروژه از یک نیاز واقعی شکل گرفت؛ جایی که سرور اصلی پروژه به دلیل شرایط شبکه نمی‌توانست ارتباط مستقیمی با سرویس‌هایی مانند Telegram API داشته باشد.

به جای ساختن یک Proxy ساده، یک لایه‌ی Application-Level طراحی شد که درخواست‌ها را امضا می‌کند و در سمت مقصد قبل از هرگونه پردازش، امضای آن‌ها را اعتبارسنجی می‌کند.

به همین دلیل، پروژه صرفاً یک Webhook Receiver ساده نیست؛ بلکه یک **لایه اعتماد بین دو Application** ایجاد می‌کند.

> **Verify. Trust. Process.**
>
> **اعتبارسنجی کن. اعتماد کن. پردازش کن.**

---

## مقاله مرتبط

اگر می‌خواهید داستان شکل‌گیری این پروژه و مسئله‌ای که باعث شد آن را بسازم بخوانید، این مقاله توضیح کامل‌تری درباره‌ی تجربه واقعی پشت پروژه ارائه می‌دهد:

[وقتی سرور ایران نمی‌تواند به Telegram API وصل شود؛ تجربه ساخت Signed Webhook Receiver](https://virgool.io/@cyberhuginn/وقتی-سرور-ایران-نمی-تواند-به-telegram-api-وصل-شود-تجربه-ساخت-signed-webhook-receiver-bkzctpcochtj)

---

## Repository

[GitHub — cyberhuginn/signed-webhook-receiver](https://github.com/cyberhuginn/signed-webhook-receiver)
