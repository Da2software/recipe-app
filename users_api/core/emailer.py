from pathlib import Path
from fastapi import HTTPException, status
from core.utils import EnvManager
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template

env = EnvManager()


async def send_email(recipients: List[str], subject: str, message: str,
                     template: str | Path, data: dict):
    host = env.get_env("MAIL_SERVER")
    sender = env.get_env("MAIL_USERNAME")
    password = env.get_env("MAIL_PASSWORD")
    with open(template, "r") as file:
        template_str = file.read()
    if not template_str:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Email templated not found!")
    jinja_template = Template(template_str)

    conf = ConnectionConfig(
        MAIL_USERNAME=sender,
        MAIL_PASSWORD=password,
        MAIL_PORT=587,
        MAIL_SERVER=host,
        MAIL_FROM=sender,
        MAIL_FROM_NAME="Recipe App",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    message = MessageSchema(
        subject=subject,
        message=message,
        recipients=recipients,  # List of recipients, as many as you can pass
        body=jinja_template.render(data),
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": True, "message": "Email Successful sent!"}
