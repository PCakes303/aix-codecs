"""RFC 8785 canonical JSON encoding and strict JSON decoding for AIX."""

from __future__ import annotations

import json
from typing import Any

import rfc8785


class CodecError(ValueError):
    """Raised when JSON cannot be encoded or decoded under the AIX codec contract."""


def canonicalize(value: Any) -> bytes:
    """Return RFC 8785 canonical UTF-8 bytes for a JSON-compatible value."""
    try:
        return rfc8785.dumps(value)
    except (TypeError, ValueError, rfc8785.CanonicalizationError) as exc:
        raise CodecError(f"value cannot be canonicalized: {exc}") from exc


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CodecError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise CodecError(f"non-standard JSON numeric constant: {value}")


def decode_json(payload: bytes | str, *, require_canonical: bool = False) -> Any:
    """Decode strict UTF-8 JSON; optionally require RFC 8785 canonical bytes."""
    if isinstance(payload, bytes):
        try:
            raw = payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise CodecError("payload is not valid UTF-8") from exc
        original = payload
    elif isinstance(payload, str):
        raw = payload
        try:
            original = payload.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CodecError("payload contains invalid Unicode") from exc
    else:
        raise CodecError("payload must be bytes or str")

    try:
        value = json.loads(
            raw,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except CodecError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise CodecError(f"invalid JSON payload: {exc}") from exc

    if require_canonical and canonicalize(value) != original:
        raise CodecError("payload is valid JSON but is not RFC 8785 canonical")

    return value
