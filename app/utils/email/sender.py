import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiofiles
import aiosmtplib
from pydantic import EmailStr

from app.conf.settings import settings


class Email:
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT

    email_host_user = settings.EMAIL_HOST_USER
    email_host_pass = settings.EMAIL_HOST_PASSWORD

    email_from = settings.DEFAULT_FROM_EMAIL

    use_tls = settings.EMAIL_USE_TLS

    path_to_html = os.path.join(os.getcwd(), "app/utils/email", "template.html")

    async def _get_html_content(self, uri: str) -> str:
        async with aiofiles.open(self.path_to_html) as f:
            html = await f.read()

        return str(html.format(uri))

    async def send(
        self, to_email: EmailStr, uri: str, subject: str = "Team-Builder"
    ) -> None:
        message = MIMEMultipart()
        message["Subject"] = subject

        message_text = await self._get_html_content(uri)

        message.attach(MIMEText(message_text, "html", "utf-8"))

        await aiosmtplib.send(
            message=message,
            sender=self.email_from,
            recipients=[to_email],
            hostname=self.email_host,
            port=self.email_port,
            username=self.email_host_user,
            password=self.email_host_pass,
            use_tls=self.use_tls,
        )
