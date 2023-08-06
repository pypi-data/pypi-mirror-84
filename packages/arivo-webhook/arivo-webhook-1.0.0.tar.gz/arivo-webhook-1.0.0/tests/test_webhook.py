from unittest import TestCase

from arivo import webhook


class WebhookSignatureUnitTest(TestCase):
    def test_invalid_signature(self):
        payload = b'test2'
        signature = 'f4e0161d698df1f37ea77cc2396ea72bdbcfa5ac179f05020c3087f27f29a540'
        secret = 'secret-1'
        with self.assertRaises(webhook.InvalidSignature):
            webhook.verify_signature(payload, signature, secret)

    def test_valid_signature(self):
        payload = b'test'
        signature = 'f4e0161d698df1f37ea77cc2396ea72bdbcfa5ac179f05020c3087f27f29a540'
        secret = 'secret-1'
        webhook.verify_signature(payload, signature, secret)

    def test_utf8_secret_signature(self):
        payload = b'test'
        signature = 'b4a2476f9191c592038cd255bc0117a091497669ab38885042924bb4b2a4165a'

        # as byte string
        secret = b'secret-1-\xc3\xa4\xc3\xb6\xc3\xaa'
        webhook.verify_signature(payload, signature, secret)

        # as unicode string
        secret = 'secret-1-äöê'
        webhook.verify_signature(payload, signature, secret)

    def test_signature_is_checked_before_payload(self):
        # to prevent possible bugs/exploits during webhook event construction, we verify the signature first
        payload = b'test'
        signature = 'f4e0161d698df1f37ea77cc2396ea72bdbcfa5ac179f05020c3087f27f29a540'
        secret = 'secret-1'

        # if the signature is ok, we receive an invalid payload
        with self.assertRaises(webhook.InvalidPayload) as e:
            webhook.construct_event(payload, signature, secret)
        self.assertIn("json decode", str(e.exception))

        # if the signature is not correct, the payload is not checked
        with self.assertRaises(webhook.InvalidSignature):
            webhook.construct_event(payload, signature + "--", secret)

    def test_none_signature(self):
        with self.assertRaises(webhook.InvalidSignature):
            webhook.verify_signature(b'test', None, b'a')
        with self.assertRaises(webhook.InvalidSignature):
            webhook.verify_signature(b'test', b'a', None)
        with self.assertRaises(webhook.InvalidSignature):
            webhook.verify_signature(b'test', None, None)


class WebhookEventUnitTest(TestCase):
    def test_construct_event_utf8(self):
        signature = "14ad3c4c3df03867b60c6f8747e3fd5587a6bee8e60b9ae0ad36f9e217e5c85f"
        secret = b'secret-1-\xc3\xa4\xc3\xb6\xc3\xaa'

        payload = b'{"\xc3\xa4": "\xc3\xaa"}'
        event = webhook.construct_event(payload, signature, secret)
        self.assertDictEqual(event, {"ä": "ê"})

    def test_payloads_must_be_bytes(self):
        # to avoid encoding-confusion, we enforce that the payload is a byte string
        payload = 'test'
        signature = 'f4e0161d698df1f37ea77cc2396ea72bdbcfa5ac179f05020c3087f27f29a540'
        secret = 'secret-1'
        with self.assertRaises(webhook.InvalidPayload) as e:
            webhook.construct_event(payload, signature, secret)
        self.assertIn("must be of type", str(e.exception))
