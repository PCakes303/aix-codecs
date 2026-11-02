# Security policy

This repository contains an experimental serialization helper. It is not a security boundary, authentication system, authorization engine, or transport.

Report suspected vulnerabilities privately to the repository maintainer rather than publishing exploit details. Do not include secrets, credentials, private keys, or sensitive operational data in issues or pull requests.

Consumers must impose payload-size and nesting-depth limits, validate decoded messages against the pinned AIX Core schema, authenticate senders independently, enforce authorization independently, and apply replay/idempotency controls at the appropriate boundary.

Canonicalization provides a deterministic representation; it does not prove origin, integrity of transit, authenticity, authorization, or truth.
