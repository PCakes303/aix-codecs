import unittest

from aix_codecs.canonical import CodecError, canonicalize, decode_json


class CanonicalCodecTests(unittest.TestCase):
    def test_object_order_and_whitespace_are_normalized(self):
        first = {"z": 1, "a": [True, None, "x"]}
        second = {"a": [True, None, "x"], "z": 1}
        self.assertEqual(canonicalize(first), canonicalize(second))
        self.assertEqual(canonicalize(first), b'{"a":[true,null,"x"],"z":1}')

    def test_rfc8785_number_serialization_vector(self):
        value = {"numbers": [333333333.33333329, 1e30, 4.50, 2e-3, 1e-27]}
        self.assertEqual(canonicalize(value), b'{"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27]}')

    def test_empty_object_key_is_valid_rfc8785_json(self):
        self.assertEqual(canonicalize({"": 1}), b'{"":1}')

    def test_negative_zero_is_canonicalized(self):
        self.assertEqual(canonicalize(-0.0), b"0")

    def test_unicode_and_control_characters(self):
        value = {"€": "A\nB", "quote": 'a"b', "slash": "\\"}
        self.assertEqual(canonicalize(value), b'{"quote":"a\\"b","slash":"\\\\","€":"A\\nB"}')

    def test_decode_round_trip(self):
        value = {"task": {"id": "task-001"}, "status": "requested"}
        self.assertEqual(decode_json(canonicalize(value)), value)

    def test_strict_mode_rejects_noncanonical_json(self):
        with self.assertRaises(CodecError):
            decode_json(b'{ "b": 2, "a": 1 }', require_canonical=True)

    def test_strict_mode_accepts_canonical_json(self):
        payload = b'{"a":1,"b":2}'
        self.assertEqual(decode_json(payload, require_canonical=True), {"a": 1, "b": 2})

    def test_duplicate_keys_and_nonstandard_numbers_are_rejected(self):
        with self.assertRaises(CodecError):
            decode_json(b'{"a":1,"a":2}')
        with self.assertRaises(CodecError):
            decode_json(b'{"value":NaN}')
        with self.assertRaises(CodecError):
            decode_json(b'{"value":1e400}')

    def test_invalid_utf8_is_rejected(self):
        with self.assertRaises(CodecError):
            decode_json(b'{"value":"\xff"}')

    def test_non_json_python_values_are_rejected(self):
        with self.assertRaises(CodecError):
            canonicalize({"not_json": object()})

    def test_byte_depth_and_container_limits(self):
        with self.assertRaisesRegex(CodecError, "byte limit"):
            decode_json(b" " * (1_048_577))
        deep = '{"x":' + ("[" * 33) + "0" + ("]" * 33) + "}"
        with self.assertRaisesRegex(CodecError, "nesting"):
            decode_json(deep)
        with self.assertRaisesRegex(CodecError, "item limit"):
            canonicalize([0] * 10_001)
        with self.assertRaisesRegex(CodecError, "property limit"):
            canonicalize({f"k{i}": 0 for i in range(10_001)})


if __name__ == "__main__":
    unittest.main()
