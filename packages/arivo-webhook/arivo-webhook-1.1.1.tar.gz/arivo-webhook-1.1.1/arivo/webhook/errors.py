class WebhookError(Exception):
    pass


class InvalidSignature(WebhookError):
    pass


class InvalidPayload(WebhookError):
    pass
