import smtplib
from jinja2 import Environment, FileSystemLoader
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.config.config import config
from app.config.logger import Logger

cloudwatch_logger = Logger.get_logger('email')


def send_mail(receiver: str, subject: str, template_name: str,
              collaborator: str, cpf: str, attachment):
    sender_email = "noreply@upperds.com"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = subject
    if attachment:
        msg = add_attachment(msg, attachment, f"boleto_{cpf}.pdf")
    smtp_server = "smtp.gmail.com"
    port = 587
    template = locate_template(template_name, collaborator, cpf)
    msg.attach(MIMEText(template, 'html'))
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, config.EMAIL_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        return True
    except Exception as ex:
        cloudwatch_logger.error(ex)
        return False


def add_attachment(msg, file, file_name):
    attachment = MIMEApplication(file, _subtype="pdf")
    attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
    msg.attach(attachment)
    return msg


def locate_template(template_name: str, collaborator: str, cpf: str):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = jinja_env.get_template(f'{template_name}.html').render(collaborator=collaborator, cpf=cpf)
    return template
