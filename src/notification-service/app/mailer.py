from email.mime.text import MIMEText
from smtplib import SMTP

from jinja2 import FileSystemLoader, Environment

from app import logger
from app.config import settings


def render_template(template_file: str, data: dict) -> str:
    """
    Function to render the template with data

    :param template_file: The relative-path to the Jinja2 template file
    :param data: The data to be populated
    :return: Template object
    """
    template_loader = FileSystemLoader(searchpath="./")
    output = Environment(loader=template_loader, autoescape=True).get_template(template_file).render(data)
    return output


def send_mail(receiver: str, subject: str, message: str):
    """
    Function to send an email

    :param receiver: The email address of the receiver
    :param subject: The subject line of the email
    :param message: The content of the email
    """
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = settings.MAIL_DEFAULT_SENDER
    msg['To'] = receiver

    # Send email
    with SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_DEFAULT_SENDER, receiver, msg.as_string())
        del msg


def notify(message):
    rendered = render_template('app/demo.html', {"mp3_fid": message["mp3_fid"]})
    send_mail(message["email"], 'Download mp3', rendered)
    logger.info("Email Sent")
