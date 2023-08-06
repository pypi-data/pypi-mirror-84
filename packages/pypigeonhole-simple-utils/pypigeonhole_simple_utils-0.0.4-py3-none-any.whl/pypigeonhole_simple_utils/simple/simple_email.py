from dataclasses import dataclass
import smtplib
from email.message import Message, EmailMessage
import email
import email.encoders
import email.mime.multipart
import email.mime.text
import email.mime.base
import os

import pypigeonhole_simple_utils.simple.network_utils as network_utils


# Abstract these fields to a class to avoid long method parameters in send()
# Headers are listed here: https://en.wikipedia.org/wiki/MIME#MIME_header_fields
@dataclass
class Envelop:  # = namedtuple('Envelop', ['subject', 'from_addr', 'to_addr', 'headers'])
    subject: str
    from_addr: str
    to_addr: str  # comma separated emails
    cc_addr: str = None  # comma separated emails
    bcc_addr: str = None  # comma separated emails
    headers: dict = None


# This is a context to handle connection close. It has 2 convenient methods to
# send text and html(check content type header). For other types, create a
# proper Message and use the generic send(). So this class handles the send()
# logic and leave the message construction outside the scope, because there
# are so many possibilities to construct different messages. We help with only
# the commonly used Message types, text and html.
class EmailServer:
    def __init__(self, email_server: network_utils.RemoteServer,
                 credential: network_utils.Credential = None):
        self._email_server = email_server
        self._credential = credential
        self._smtp_sender = None

    def __enter__(self):
        if self._email_server.port == 465:
            self._smtp_sender = smtplib.SMTP_SSL(self._email_server.address())

            if self._credential:
                self._smtp_sender.login(self._credential.user, self._credential.password)
        else:  # 25 or 587
            self._smtp_sender = smtplib.SMTP(self._email_server.address())

            if self._credential:
                self._smtp_sender.login(self._credential.user, self._credential.password)
            else:
                self._smtp_sender.starttls()

        return self._smtp_sender

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._smtp_sender.quit()

    def send_text(self, text, envelop: Envelop):
        msg = Message()
        msg.set_payload(text)
        msg.add_header('Content-Type', 'text/html')
        return self.send(msg, envelop)

    def send_html(self, html, envelop: Envelop, alt_text=None):
        msg = EmailMessage()
        msg.set_payload(html)
        msg.add_header('Content-Type', 'text/html')
        if alt_text:
            msg.add_alternative(alt_text, 'plain')

        return self.send(msg, envelop)

    def send_attachment(self, message, files, envelop: Envelop):
        msg = email.mime.multipart.MIMEMultipart('alternative')

        if message:
            msg.attach(email.mime.text.MIMEText(message))

        if files:
            for f in files:
                with open(f, "rb") as fil:
                    attachment = email.mime.base.MIMEBase('appliction', 'octet-stream')
                    attachment.set_payload(fil.read())
                    email.encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition',
                                          'attachment; filename="%s"' % os.path.basename(f))

                    msg.attach(attachment)
        return self.send(msg, envelop)

    def send(self, message: Message, envelop: Envelop):
        message['Subject'] = envelop.subject
        message['From'] = envelop.from_addr
        message['To'] = envelop.to_addr

        if envelop.cc_addr:
            message['Cc'] = envelop.cc_addr
        if envelop.bcc_addr:
            message['Bcc'] = envelop.bcc_addr

        if envelop.headers:
            for k, v in envelop.headers.items():
                if k in message:
                    message.replace_header(k, v)
                else:
                    message.add_header(k, v)

        # https://pybit.es/python-MIME-bcc.html
        return self._smtp_sender.send_message(message)


# email.mime has a few submodules to deal with text, multipart for text,
# attachments, etc. Here we only make simple things. For other combinations,
# such as text + attachment, html + attachments, we leave it out.
