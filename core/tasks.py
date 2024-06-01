from django.core.mail import send_mail

from accounts.send_mail import send_confirmation_email
from .celery import app


@app.task
def send_confirmation_email_task(user, code):
    send_confirmation_email(user, code)


@app.task
def send_password_reset_email(email, code):
    send_mail(
        'Password Reset Request',
        f'Your password reset code is: {code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )
