from celery import shared_task
from django.core.mail import send_mail


@shared_task  # благодоря данному декоратору, celery поймет, что нужно выполнять данную задачу
def send_activation_mail(email, activation_code):
    message = f'Ваш код активации {activation_code}'
    send_mail('Активация аккаунта', message, 'test@test.com', [email])


