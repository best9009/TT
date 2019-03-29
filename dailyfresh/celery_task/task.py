from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time
app = Celery('celery_task.task', broker='redis://127.0.0.1:6379/9')

@app.task
def celery_task_send_mail(recip_email, mess):
    subject = '天天生鲜欢迎信息'
    message = ''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recip_email]
    html_message = mess
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    time.sleep(20)