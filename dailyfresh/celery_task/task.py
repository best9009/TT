from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time
from django.template.loader import get_template
import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner


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
@app.task
def static_index_html_load():
    # 获取所有商品的种类
    types = GoodsType.objects.all()
    # 获取滚动的商品
    index_goods_banner = IndexGoodsBanner.objects.all().order_by('index')
    # 获取促销商品
    index_promotion_banner = IndexPromotionBanner.objects.all().order_by('index')
    for type in types:
        tittle_goods_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
        image_goods_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        type.tittle_goods_banner = tittle_goods_banner
        type.image_goods_banner = image_goods_banner

    context = {'types':types,
               'index_goods_banner': index_goods_banner,
               'index_promotion_banner': index_promotion_banner
               }
    temp = get_template('static_index.html')
    index_static_html = temp.render(context)
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path) as f:
        f.write(index_static_html, 'w')