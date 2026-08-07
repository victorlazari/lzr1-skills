# n8n Security Best Practices

Verified against upstream: 2026-08-07

## Credential Management

- **n8n Credential Manager**: Always use n8n's built-in credential manager to store API keys, tokens, and passwords. Never hardcode credentials in workflow nodes.
- **Encryption Key**: Ensure the `N8N_ENCRYPTION_KEY` environment variable is set to a strong, unique value. This key encrypts all credentials stored in the database.

## Webhook Authentication

- **Authentication**: Always configure authentication for Webhook nodes. Use Basic Auth or Header Auth to prevent unauthorized access to your workflows.
- **Validation**: Validate incoming payloads to ensure they conform to expected schemas before processing them.

## General Security

- **Least Privilege**: Grant n8n only the permissions necessary to perform its tasks across integrated services.
- **Network Security**: Deploy n8n behind a reverse proxy (e.g., Nginx, Traefik) with TLS/SSL enabled. Restrict access to the n8n UI and webhook endpoints using firewalls or VPNs if appropriate.
