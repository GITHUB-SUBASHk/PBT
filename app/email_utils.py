# app/email_utils.py

import os
from dotenv import load_dotenv
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import aiosmtplib

load_dotenv()

MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Set up Jinja2 environment for loading templates
template_loader = FileSystemLoader("app/templates")
jinja_env = Environment(loader=template_loader)

def send_verification_email(to_email: str, token: str):
    subject = "Verify your email to set password"
    verify_link = f"{FRONTEND_URL}/set-password/{token}"

    template = jinja_env.get_template("verify_email.html")
    content = template.render(link=verify_link)

    send_email(to_email, subject, content)

def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP for password reset"
    template = jinja_env.get_template("reset_email.html")
    content = template.render(otp=otp)

    send_email(to_email, subject, content)

def send_email(to_email: str, subject: str, html_content: str):
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content("This is an HTML email.")
    message.add_alternative(html_content, subtype="html")

    # Send using SMTP (MailHog in local)
    try:
        aiosmtplib.send(
            message,
            hostname=MAIL_SERVER,
            port=MAIL_PORT
        )
    except Exception as e:
        print("Email send failed:", e)
