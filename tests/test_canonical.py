import unittest

from aix_codecs.canonical import CodecError, canonicalize, decode_json


class CanonicalCodecTests(unittest.TestCase):
    def test_object_order_and_whitespace_are_normalized(self):
        first = {"z": 1, "a": [True, None, "x"]}
        second = {"a": [True, None, "x"], "z": 1}
        self.assertEqual(canonicalize(first), canonicalize(second))
        self.assertEqual(canonicalize(first), b'{"a":[true,null,"x"],"z":1}')

    def test_decode_round_trip(self):
        value = {"task": {"id": "task-001"}, "status": "requested"}
        self.assertEqual(decode_json(canonicalize(value)), value)

    def test_strict_mode_rejects_noncanonical_json(self):
        with self.assertRaises(CodecError):
            decode_json(b'{ "b": 2, "a": 1 }', require_canonical=True)

    def test_strict_mode_accepts_canonical_json(self):
        payload = b'{"a":1,"b":2}'
        self.assertEqual(decode_json(payload, require_canonical=True), {"a": 1, "b": 2})

    def test_duplicate_keys_are_rejected(self):
        with self.assertRaises(CodecError):
            decode_json(b'{"a":1,"a":2}')

    def test_nonstandard_numbers_are_rejected(self):
        with self.assertRaises(CodecError):
            decode_json(b'{"value":NaN}')

    def test_invalid_utf8_is_rejected(self):
        with self.assertRaises(CodecError):
            decode_json(b'{"value":"\xff"}')

    def test_non_json_python_values_are_rejected(self):
        with self.assertRaises(CodecError):
            canonicalize({"not_json": object()})


if __name__ == "__main__":
    unittest.main()
