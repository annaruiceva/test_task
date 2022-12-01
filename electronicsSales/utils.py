import datetime

import qrcode

import random
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import random

from celery import shared_task
# from django_celery_results.models import TaskResult
# TaskResult.objects.last()
from celery.schedules import crontab
from django.db.models import F

from electronicsSales import models
from rocketData.celery import app

from rocketData.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, \
    EMAIL_HOST_PORT


def create_qr_code(value):
    new_img = qrcode.make(value)
    filename = 'media/qr-code/QR-code' + str(datetime.datetime.now().strftime('%d-%m-%Y--%H-%M')) + '.png'
    try:
        new_img.save(filename)
    except:
        return ''
    return filename
