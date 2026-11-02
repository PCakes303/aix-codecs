# Agent and contributor instructions

- Treat AIX Core as the authority for message semantics; this repository owns byte encoding only.
- Implement canonical JSON using RFC 8785. Do not substitute ordinary sorted JSON serialization.
- Reject duplicate keys, invalid UTF-8, malformed JSON, and non-standard numeric constants.
- Never add authentication, authorization, transport, or trust claims to codec behavior.
- Do not serialize private model reasoning or chain-of-thought.
- Add positive and negative vectors for every behavior change.
- Keep errors explicit and fail closed; never silently repair malformed input.
- Do not claim cross-language conformance until an independent implementation passes shared vectors.
- License remains pending review; do not add a license file or infer a license.
- Run `python -m unittest discover -s tests -v` before proposing changes.
