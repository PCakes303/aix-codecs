# AIX Codecs — Repository 12 build packet

**Portfolio position:** 12 / 29 public repositories  
**Repository name:** `aix-codecs`  
**Layer:** Protocols  
**Maturity:** prepared scaffold; not yet deployed to its standalone remote  
**Depends on:** `aix-core`, `agent-schema-registry`

## Mission

Provide deterministic, interoperable serialization and decoding for AIX messages. This repository implements the encoding boundary for the AIX semantic contract; it does not redefine AIX message meaning, transport messages, authenticate senders, or authorize actions.

## Architecture constraints

- AIX remains an extension layer over MCP, A2A, HTTP, JSON-RPC, and existing transports.
- Canonical JSON follows RFC 8785 (JSON Canonicalization Scheme); do not invent a custom canonicalization algorithm.
- Decoding rejects invalid UTF-8, malformed JSON, duplicate object keys, and non-standard numeric constants.
- Optional strict mode verifies that incoming bytes are already canonical.
- Codec operations are deterministic and side-effect free.
- Schema validation is a separate concern and must use the versioned AIX Core schema.
- No private model reasoning or chain-of-thought fields are defined or serialized.

## Initial build contents

- `aix_codecs/canonical.py` — canonical encode/decode reference implementation.
- `tests/test_canonical.py` — deterministic, malformed-input, duplicate-key, and canonical-form tests.
- `requirements-dev.txt` — pinned development dependencies.
- `docs/CODEC-CONTRACT.md` — normative codec behavior and error model.
- `.github/workflows/ci.yml` — test workflow.

## Local validation

Requires Python 3.10+.

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## Build gates

1. **Scaffold:** canonical encode/decode behavior, error handling, test vectors, CI.
2. **Experimental:** schema-bound AIX message codec, cross-language vectors, fuzz/property tests, size/depth limits.
3. **Alpha:** at least two independent implementations produce byte-identical canonical output; compatibility tests against a pinned AIX Core schema.
4. **Stable:** reviewed security model, reproducible artifacts, signed release provenance, migration policy, and conformance evidence.

No production, cross-language conformance, or release claim is made by this prepared packet.

## Dependencies

- [AIX Core](https://github.com/PCakes303/aix-core) owns message semantics and schemas.
- [Agent Schema Registry](https://github.com/PCakes303/agent-schema-registry) owns schema versioning and compatibility rules.
- [Master registry](https://github.com/PCakes303/agent-intelligence-ecosystem) owns portfolio scope and dependencies.

## License

Pending the ecosystem's mixed-license review. Do not add a license file until the repository-specific license decision is approved.
