import random
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task
# from django_celery_results.models import TaskResult
# TaskResult.objects.last()
from django.db.models import F

from electronicsSales import models
from rocketData.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, \
    EMAIL_HOST_PORT


#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10800, add_debt.s(), name='add every 3 hours')
#     sender.add_periodic_task(
#         crontab(hour=6, minute=30),
#         sub_debt.s(),
#     )

# добавила periodic_tasks через админ-панель
@shared_task
def add_debt():
    models.Element.objects.all().update(debt=F('debt') + random.randint(5, 500))
    return 'debt added'


@shared_task
def sub_debt():
    models.Element.objects.all().update(debt=F('debt') - random.randint(100, 10000))
    return 'debt sub'


@shared_task
def update_queryset(id):
    models.Element.objects.filter(id=id).update(debt=0)
    return 'debt 0'


@shared_task(name="send_email_task",
             ignore_result=True)
def send_email(user_id, img_name):
    user = models.User.objects.get(id=user_id)
    msg = MIMEMultipart()
    msg['Subject'] = 'Тема письма'
    msg['From'] = DEFAULT_FROM_EMAIL

    part = MIMEText('Текст письма\n')
    msg.attach(part)

    part = MIMEApplication(open(img_name, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=img_name)
    msg.attach(part)

    server = smtplib.SMTP(EMAIL_HOST_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    server.sendmail(msg['From'], user.email, msg.as_string())
