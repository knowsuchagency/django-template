import base64
import json
import logging
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

CF_URL = "https://api.cloudflare.com/client/v4/accounts/{account_id}/email/sending/send"


class CloudflareEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.account_id = getattr(settings, "CLOUDFLARE_ACCOUNT_ID", "")
        self.api_token = getattr(settings, "CLOUDFLARE_API_TOKEN", "")
        self.timeout = getattr(settings, "CLOUDFLARE_EMAIL_TIMEOUT", 30)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        if not (self.account_id and self.api_token):
            if self.fail_silently:
                return 0
            raise RuntimeError(
                "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set"
            )
        sent = 0
        for msg in email_messages:
            try:
                self._send(msg)
                sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
                logger.exception("cloudflare_email_send_failed")
        return sent

    def _send(self, msg):
        payload = _build_payload(msg)
        req = urllib.request.Request(
            CF_URL.format(account_id=self.account_id),
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            resp.read()


def _build_payload(msg):
    payload = {
        "from": msg.from_email,
        "to": list(msg.to),
        "subject": msg.subject,
    }
    if msg.cc:
        payload["cc"] = list(msg.cc)
    if msg.bcc:
        payload["bcc"] = list(msg.bcc)
    if msg.reply_to:
        payload["reply_to"] = msg.reply_to[0] if len(msg.reply_to) == 1 else list(msg.reply_to)

    if msg.content_subtype == "html":
        payload["html"] = msg.body
    else:
        payload["text"] = msg.body

    for content, mimetype in getattr(msg, "alternatives", []):
        if mimetype == "text/html":
            payload["html"] = content
            break

    # Attachments arrive as (filename, content, mimetype); Cloudflare expects base64-encoded content.
    attachments = []
    for attachment in msg.attachments:
        if isinstance(attachment, tuple):
            filename, content, mimetype = attachment
        else:
            filename = attachment.get_filename() or ""
            content = attachment.get_payload(decode=True) or b""
            mimetype = attachment.get_content_type()
        if isinstance(content, str):
            content = content.encode("utf-8")
        attachments.append(
            {
                "filename": filename or "attachment",
                "content": base64.b64encode(content).decode("ascii"),
                "type": mimetype or "application/octet-stream",
            }
        )
    if attachments:
        payload["attachments"] = attachments

    if msg.extra_headers:
        payload["headers"] = dict(msg.extra_headers)

    return payload
