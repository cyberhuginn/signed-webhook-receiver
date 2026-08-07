# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please do not open a public GitHub issue.

Instead, report it privately with the following information:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any relevant logs or screenshots

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅ |
| Older versions | ❌ |

## Security Considerations

This project uses RSA signature verification to validate incoming webhook payloads.

Please ensure:

- Private keys are never exposed to the receiver
- Public keys are stored securely
- HTTPS is used in production
- Payload timestamps are used to prevent replay attacks
- Keys are rotated periodically

## Contact

For security reports, contact:

security@cyberhuginn.com