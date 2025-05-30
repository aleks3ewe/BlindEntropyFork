#!/usr/bin/env python3
"""
AES-256-GCM helper.
encrypt_task_id(key_hex: str, task_id: int) -> str
decrypt_task_id(key_hex: str, ciphertext_b64: str) -> int
"""
import base64
import secrets

from Crypto.Cipher import AES

_NONCE_LEN = 12
_TAG_LEN = 16
_CT_LEN = 1


def _key_from_hex(hex_key: str) -> bytes:
    key = bytes.fromhex(hex_key)
    if len(key) != 32:
        raise ValueError("Need 256-bit (64-hex) key")
    return key


def encrypt_task_id(key_hex: str, task_id: int) -> str:
    if not (1 <= task_id <= 25):
        raise ValueError("task_id must be in 1…25")

    key = _key_from_hex(key_hex)
    nonce = secrets.token_bytes(_NONCE_LEN)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(task_id.to_bytes(_CT_LEN, "big"))

    bundle = nonce + tag + ct
    return base64.b64encode(bundle).decode("ascii")


def decrypt_task_id(key_hex: str, ciphertext_b64: str) -> int:
    raw = base64.b64decode(ciphertext_b64)

    nonce = raw[:_NONCE_LEN]
    tag = raw[_NONCE_LEN:_NONCE_LEN + _TAG_LEN]
    ct = raw[_NONCE_LEN + _TAG_LEN:]

    if len(ct) != _CT_LEN:
        raise ValueError("Ciphertext length mismatch")

    key = _key_from_hex(key_hex)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return int.from_bytes(pt, "big")
