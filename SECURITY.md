# Security Policy

This repository contains an experimental RFC 8785 serialization and strict JSON decoding helper. It is not a security boundary, authentication system, authorization engine, transport, or trusted audit mechanism.

## Reporting

Do not publish exploitable vulnerabilities, credentials, private keys, or sensitive operational data in public issues. Use GitHub private vulnerability reporting or a private security advisory if enabled for this repository. A dedicated private reporting address is not published here; if private reporting is unavailable, the owner must configure an owner-approved private channel before production use.

## Consumer responsibilities

- Enforce payload byte-size and nesting-depth limits before decoding untrusted input.
- Validate decoded messages against a pinned AIX Core schema.
- Authenticate senders and authorize actions independently.
- Apply replay and idempotency protections at the appropriate boundary.
- Treat canonicalization as deterministic representation only; it does not prove origin, transit integrity, authenticity, authorization, or truth.
- Never serialize private model reasoning or chain-of-thought.
