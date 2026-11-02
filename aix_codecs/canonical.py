"""RFC 8785 canonical JSON encoding and bounded strict JSON decoding for AIX."""

from __future__ import annotations

import json
import math
from typing import Any

import rfc8785

MAX_PAYLOAD_BYTES = 1_048_576
MAX_JSON_DEPTH = 32
MAX_CONTAINER_ITEMS = 10_000
MAX_OBJECT_KEY_LENGTH = 4096


class CodecError(ValueError):
    """Raised when JSON cannot be encoded or decoded under the AIX codec contract."""


def _validate_value(value: Any, depth: int = 0) -> None:
    if depth > MAX_JSON_DEPTH:
        raise CodecError("JSON nesting exceeds depth limit")
    if isinstance(value, dict):
        if len(value) > MAX_CONTAINER_ITEMS:
            raise CodecError("JSON object exceeds property limit")
        for key, item in value.items():
            if not isinstance(key, str) or not key or len(key) > MAX_OBJECT_KEY_LENGTH:
                raise CodecError("JSON object keys must be non-empty bounded strings")
            _validate_value(item, depth + 1)
    elif isinstance(value, list):
        if len(value) > MAX_CONTAINER_ITEMS:
            raise CodecError("JSON array exceeds item limit")
        for item in value:
            _validate_value(item, depth + 1)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise CodecError("non-finite JSON numbers are prohibited")
    elif value is None or isinstance(value, (str, bool, int)):
        return
    else:
        raise CodecError(f"unsupported JSON value type: {type(value).__name__}")


def _check_raw_depth(raw: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in raw:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise CodecError("JSON nesting exceeds depth limit")
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise CodecError("invalid JSON structure")


def canonicalize(value: Any) -> bytes:
    """Return RFC 8785 canonical UTF-8 bytes for a bounded JSON-compatible value."""
    _validate_value(value)
    try:
        encoded = rfc8785.dumps(value)
    except (TypeError, ValueError, OverflowError, RecursionError, rfc8785.CanonicalizationError) as exc:
        raise CodecError(f"value cannot be canonicalized: {exc}") from exc
    if len(encoded) > MAX_PAYLOAD_BYTES:
        raise CodecError("canonical JSON exceeds byte limit")
    return encoded


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
    """Decode bounded strict UTF-8 JSON; optionally require RFC 8785 canonical bytes."""
    if isinstance(payload, bytes):
        if len(payload) > MAX_PAYLOAD_BYTES:
            raise CodecError("payload exceeds byte limit")
        try:
            raw = payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise CodecError("payload is not valid UTF-8") from exc
        original = payload
    elif isinstance(payload, str):
        try:
            original = payload.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CodecError("payload contains invalid Unicode") from exc
        if len(original) > MAX_PAYLOAD_BYTES:
            raise CodecError("payload exceeds byte limit")
        raw = payload
    else:
        raise CodecError("payload must be bytes or str")

    _check_raw_depth(raw)
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

    _validate_value(value)
    if require_canonical and canonicalize(value) != original:
        raise CodecError("payload is valid JSON but is not RFC 8785 canonical")
    return value
