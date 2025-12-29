# Hybrid Connectivity Bridge

[![CI](https://github.com/cmangun/hybrid-connectivity-bridge/actions/workflows/ci.yml/badge.svg)](https://github.com/cmangun/hybrid-connectivity-bridge/actions/workflows/ci.yml)

Secure bridge pattern for hybrid connectivity between restricted networks and cloud services.

## Overview

This repository demonstrates a secure "handoff" pattern for moving data between trust boundaries (on-premises ↔ cloud) using signed bundles and staged transfers.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    On-Premises Zone                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   TypeScript Producer                     │   │
│  │  Source Data → Sign → Bundle → Stage to Local Folder     │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
                              │
                              │ Secure Transfer (staged files)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Cloud Zone                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Python Consumer                        │   │
│  │  Read Bundle → Verify Signature → Process → Output        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Components

| Component | Language | Purpose |
|-----------|----------|---------|
| `bridge/ts-producer` | TypeScript | Creates signed bundles |
| `bridge/py-consumer` | Python | Validates and processes bundles |
| `shared/schema` | JSON Schema | Bundle format specification |

## Quickstart

```bash
# Install dependencies
cd bridge/ts-producer && npm install && cd ../..
cd bridge/py-consumer && pip install -r requirements.txt && cd ../..

# Run demo
make demo
```

## Bundle Format

```json
{
  "bundleId": "uuid",
  "createdAt": "ISO-8601",
  "producer": "producer-id",
  "payload": { ... },
  "signature": "base64-signature",
  "checksum": "sha256-hash"
}
```

## Security Features

- **Signed bundles**: HMAC signatures on all transfers
- **Checksums**: SHA-256 integrity verification
- **Audit trail**: Every bundle logged with correlation ID
- **Validation**: Schema validation at boundary crossing

## Next Iterations

- [ ] Add asymmetric signatures (RSA/ECDSA)
- [ ] Add S3/Azure Blob transfer adapters
- [ ] Add retry/dead-letter handling
- [ ] Add encryption at rest
- [ ] Add batch processing mode
- [ ] Add Kubernetes Job templates

## License

MIT © Christopher Mangun

---

**Portfolio**: [field-deployed-engineer.vercel.app](https://field-deployed-engineer.vercel.app/)  
**Contact**: Christopher Mangun — Brooklyn, NY
