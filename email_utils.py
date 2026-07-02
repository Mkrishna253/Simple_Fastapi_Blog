from email.message import EmailMessage
import asyncio
from functools import lru_cache
import smtplib
import ssl

import certifi
from fastapi.templating import Jinja2Templates

from config import settings

templates = Jinja2Templates(directory="templates")
password_reset_template = templates.env.get_template("email/password_reset.html")


@lru_cache(maxsize=1)
def _resolve_encryption_mode() -> str:
    mode = settings.mail_encryption.strip().lower()
    if mode in {"ssl", "starttls", "none"}:
        return mode
    return "starttls" if settings.mail_use_tls else "none"


@lru_cache(maxsize=1)
def _build_tls_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if settings.mail_validate_certs:
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=certifi.where())
    else:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context


def _send_email_sync(message: EmailMessage) -> None:
    """Send email using synchronous smtplib from a thread executor."""
    context = _build_tls_context()
    encryption_mode = _resolve_encryption_mode()

    if encryption_mode == "ssl":
        with smtplib.SMTP_SSL(
            settings.mail_server,
            settings.mail_port,
            timeout=settings.mail_timeout_seconds,
            context=context,
        ) as smtp:
            if settings.mail_username:
                smtp.login(
                    settings.mail_username,
                    settings.mail_password.get_secret_value(),
                )
            smtp.send_message(message)
        return

    with smtplib.SMTP(
        settings.mail_server,
        settings.mail_port,
        timeout=settings.mail_timeout_seconds,
    ) as smtp:
        smtp.ehlo()
        if encryption_mode == "starttls":
            smtp.starttls(context=context)
            smtp.ehlo()
        if settings.mail_username:
            smtp.login(
                settings.mail_username,
                settings.mail_password.get_secret_value(),
            )
        smtp.send_message(message)


def _is_transient_smtp_error(exc: Exception) -> bool:
    if isinstance(
        exc,
        (
            smtplib.SMTPServerDisconnected,
            smtplib.SMTPConnectError,
            smtplib.SMTPHeloError,
            TimeoutError,
            OSError,
        ),
    ):
        return True
    if isinstance(exc, smtplib.SMTPResponseException):
        # 4xx SMTP responses are temporary failures and can often succeed on retry.
        return 400 <= exc.smtp_code < 500
    return False


async def send_email(
    to_email: str,
    subject: str,
    plain_text: str,
    html_content: str | None = None,
) -> None:
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(plain_text)

    if html_content:
        message.add_alternative(html_content, subtype="html")

    loop = asyncio.get_running_loop()
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            await loop.run_in_executor(None, _send_email_sync, message)
            return
        except Exception as exc:
            if not _is_transient_smtp_error(exc) or attempt == max_attempts - 1:
                raise
            await asyncio.sleep(0.5 * (2**attempt))


async def send_password_reset_email(to_email: str, username: str, token: str) -> None:
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"

    html_content = password_reset_template.render(reset_url=reset_url, username=username)

    plain_text = f"""Hi {username},

You requested to reset your password. Click the link below to set a new password:

{reset_url}

This link will expire in 1 hour.

If you didn't request this, you can safely ignore this email.

Best regards,
The FastAPI Blog Team
"""

    await send_email(
        to_email=to_email,
        subject="Reset Your Password - FastAPI Blog",
        plain_text=plain_text,
        html_content=html_content,
    )