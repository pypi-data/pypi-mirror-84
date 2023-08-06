import hashlib
import hmac
import json


class WebhookError(Exception):
    pass


class InvalidSignature(WebhookError):
    pass


class InvalidPayload(WebhookError):
    pass


class Event(dict):
    pass


def construct_event(payload, signature, secret):
    if not isinstance(payload, bytes):
        raise InvalidPayload("payload must be of type 'bytes'")
    verify_signature(payload, signature, secret)
    event = decode_payload(payload)
    return event


def verify_signature(payload, signature, secret):
    if not signature:
        raise InvalidSignature

    if hasattr(secret, "encode"):
        secret = secret.encode()

    if signature is None or secret is None:
        raise InvalidSignature()

    compare_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, compare_signature):
        raise InvalidSignature()


def decode_payload(payload):
    if hasattr(payload, "decode"):
        payload = payload.decode("utf-8")

    try:
        payload = json.loads(payload)
    except json.JSONDecodeError as e:
        raise InvalidPayload('json decode error: {}'.format(e.msg))

    return payload
