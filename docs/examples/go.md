# Go Webhook Sender

This example shows how to generate a signed webhook payload using Go.

The sender uses:

- Go standard crypto packages
- RSA private key
- SHA-256 hashing
- PKCS#1 v1.5 padding
- Base64 encoded signature

## Requirements

Go 1.22+

## Example

```go
package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"fmt"
	"os"
)


func main() {

	data := `{"event":"payment.completed","id":123}`


	privateKeyData, err := os.ReadFile(
		"private.pem",
	)

	if err != nil {
		panic(err)
	}


	block, _ := pem.Decode(
		privateKeyData,
	)


	privateKey, err := x509.ParsePKCS1PrivateKey(
		block.Bytes,
	)

	if err != nil {
		panic(err)
	}


	hash := sha256.Sum256(
		[]byte(data),
	)


	signature, err := rsa.SignPKCS1v15(
		rand.Reader,
		privateKey,
		crypto.SHA256,
		hash[:],
	)

	if err != nil {
		panic(err)
	}


	sign := base64.StdEncoding.EncodeToString(
		signature,
	)


	payload := fmt.Sprintf(
		`{
			"sign":"%s",
			"data":{
				"event":"payment.completed",
				"id":123
			}
		}`,
		sign,
	)


	fmt.Println(payload)
}
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
SHA-256 hash
 |
 v
RSA PKCS#1 v1.5
 |
 v
Base64 signature
```
The private key stays on the sender side.

The receiver only requires the public key for verification.