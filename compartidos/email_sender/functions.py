from typing import List

from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render
from django.utils.html import strip_tags
from rest_framework.response import Response

from configuracion.settings import (
    # EMAIL_HOST_USER,
    # EMAIL_HOST_PASSWORD,
    # EMAIL_HOST,
    # EMAIL_PORT,
    # EMAIL_USE_TLS,
    DEFAULT_FROM_EMAIL,
)


def send_email_notification(subject: str, body: str, to: List[str]) -> Response:
    """
    This function allows sending a raw text body email alert to a list of email addresses
    :params:
    :subject: str
    :body: str
    :to: List[str]

    :return: Response(200, "Email sent successfully")
    :error: Response(500, "Error sending email notification")
    """

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=to,
            fail_silently=False,
        )
        return Response("Email sent successfully", 200)
    except Exception as e:
        print(f"Error sending email notification: {e}")
        return Response("Error sending email notification", 400)


def send_email_notification_html(subject: str, to: List[str], html_template: str, context: dict) -> Response:
    """
    This function allows sending a html body email alert to a list of email addresses
    :params:
    :subject: str
    :to: List[str]
    :html_template: str -> path to html where the email structure body is defined
    :context: dict -> context to render the html template

    :return: Response(200, "Email sent successfully")
    :error: Response(500, "Error sending email notification")
    """

    try:
        body = render(html_template, context)
        plain_body = strip_tags(body)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=DEFAULT_FROM_EMAIL,
            to=to,
        )
        msg.attach_alternative(body, "text/html")
        msg.send()
        return Response(200, "Email sent successfully")
    except Exception as e:
        print(f"Error sending email notification: {e}")
        return Response(500, "Error sending email notification")
