import logging

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.settings = get_settings()

    def send(self, to_email: str, subject: str, body: str) -> bool:
        provider = (self.settings.email_provider or "disabled").lower()
        if provider == "disabled":
            logger.info("Email disabled. Would send to %s: %s", to_email, subject)
            return False
        if provider == "console":
            logger.info("EMAIL to=%s subject=%s body=%s", to_email, subject, body)
            return True
        if provider == "resend":
            return self._send_resend(to_email, subject, body)
        logger.info("Provider '%s' not wired yet. Would send to %s: %s", provider, to_email, subject)
        return False

    def _send_resend(self, to_email: str, subject: str, body: str) -> bool:
        if not self.settings.resend_api_key or not self.settings.email_from:
            logger.warning("Resend email requested but RESEND_API_KEY or EMAIL_FROM is missing.")
            return False
        try:
            response = httpx.post(
                "https://api.resend.com/emails",
                headers={
                    "authorization": f"Bearer {self.settings.resend_api_key}",
                    "content-type": "application/json",
                },
                json={
                    "from": self.settings.email_from,
                    "to": [to_email],
                    "subject": subject,
                    "text": body,
                },
                timeout=10,
            )
            if response.status_code >= 400:
                logger.warning("Resend email failed with %s: %s", response.status_code, response.text)
                return False
            return True
        except Exception as exc:
            logger.warning("Resend email failed: %s", exc)
            return False
