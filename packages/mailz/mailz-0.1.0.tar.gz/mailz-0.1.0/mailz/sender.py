from typing import Any, Dict, Iterable, Iterator

from python_http_client.client import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SendGridMail

from mailz.mail import Mail


class Sender:
    def __init__(self, config: Dict[str, Any]) -> None:
        self._client = SendGridAPIClient(config["api_key"])
        self._email = config["email"]
        self._replyto = config["replyto"]

    def send(self, emails: Iterable[Mail]) -> Iterator[Response]:
        for email in emails:
            sendgrid_email = SendGridMail(
                from_email=self._email,
                to_emails=",".join(email.to),
                subject=email.subject,
                plain_text_content=email.body,
            )
            if email.bcc:
                sendgrid_email.bcc = ",".join(email.bcc)
            if email.cc:
                sendgrid_email.cc = ",".join(email.cc)
            for key, value in email.headers.items():
                sendgrid_email.add_header({key: value})
            sendgrid_email.reply_to = self._replyto
            print(sendgrid_email.get())
            yield self._client.send(sendgrid_email)
