import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)


def send_email(from_email, to_emails, subject, html_content):
    """
    email client to send emails

    :param from_email: string - sender email
    :param to_emails: string - recipient email(s)
    :param subject: string - email subject
    :param html_content: - html content
    :return: response: object
    """
    message = Mail(
        from_email,to_emails,subject,html_content
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response
    except Exception as e:
        return e.message

