#!/usr/bin/env python3
"""
AES-256-GCM helper!
encrypt_task_id(key_hex: str, task_id: int) -> str
decrypt_task_id(key_hex: str, ciphertext_b64: str) -> int
"""

import base64
import secrets
from Crypto.Cipher import AES


def _to_bytes(hex_key: str) -> bytes:
    key = bytes.fromhex(hex_key)
    if len(key) != 32:
        raise ValueError("256! 64 hex needed!")
    return key


def encrypt_task_id(key_hex: str, task_id: int) -> str:
    key = _to_bytes(key_hex)
    nonce = secrets.token_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(task_id.to_bytes(1, "big"))
    bundle = b"|".join([nonce, tag, ct])
    return base64.b64encode(bundle).decode()


def decrypt_task_id(key_hex: str, ciphertext_b64: str) -> int:
    key = _to_bytes(key_hex)
    nonce, tag, ct = base64.b64decode(ciphertext_b64).split(b"|")
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return int.from_bytes(pt, "big")
