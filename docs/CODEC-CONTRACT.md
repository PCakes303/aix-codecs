# AIX Codec Contract

**Status:** initial implementation contract  
**Scope:** canonical JSON encoding and strict JSON decoding for AIX payloads.

## Responsibilities

The codec converts JSON-compatible AIX data into a deterministic byte representation and parses bytes back into data. It does not validate the full AIX message schema, establish publisher identity, verify signatures, authorize operations, or deliver messages.

## Canonicalization

The canonical encoder MUST implement RFC 8785 (JSON Canonicalization Scheme). It MUST NOT rely on ordinary `json.dumps(sort_keys=True)` as a substitute for RFC 8785. The implementation MUST reject values outside the JSON data model and surface a stable codec error.

The encoder returns UTF-8 bytes. Equivalent JSON data structures MUST produce identical canonical bytes within the RFC 8785 rules.

## Decoding

The decoder MUST:
- accept UTF-8 bytes or a UTF-8 string;
- reject invalid UTF-8 and malformed JSON;
- reject duplicate object member names;
- reject NaN, Infinity, and -Infinity;
- optionally require the input bytes to equal the canonical encoding;
- preserve JSON scalar, array, and object semantics.

## Error behavior

Codec errors are explicit exceptions derived from `ValueError`. Callers MUST fail closed when decoding fails. A codec error MUST NOT be converted into an empty message, default task, or permissive fallback.

## Security and resource limits

The first reference implementation is a local library helper, not a hostile-input network service. Any transport-facing integration MUST add explicit maximum payload size, nesting-depth limits, time/resource budgets, replay controls, and schema validation before processing a decoded message.

## Conformance vectors

Every implementation must share positive and negative fixtures covering:
- object-key ordering;
- whitespace normalization;
- Unicode strings;
- number serialization edge cases defined by RFC 8785;
- arrays and nested objects;
- malformed JSON and invalid UTF-8;
- duplicate keys and non-standard numeric constants;
- strict rejection of non-canonical input.

## Compatibility

AIX Core owns the semantic envelope and task lifecycle. AIX Codecs owns deterministic byte representation only. Breaking changes to the data model belong in AIX Core and must follow schema-registry compatibility policy; codec changes must preserve RFC 8785 behavior.
