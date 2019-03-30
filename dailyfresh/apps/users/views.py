
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
import re
from users.models import User, Address
from goods.models import GoodsSKU
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_task.task import celery_task_send_mail
from util.mixin import MixInClass
from django_redis import get_redis_connection

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        #验证接收到的字符是否合法
        if not all([username, password, cpassword, email]):
            return render(request, 'register.html', {'errormag':'输入的信息不完整，请重新输入'})
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormag':'邮箱格式不对'})
        if allow != 'on':
            return render(request, 'register.html', {'errormag': '请同意协议'})
        if password != cpassword:
            return render(request, 'register.html', {'errormag': '两次输入的密码不一致'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errormag': '用户名以存在'})
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        #生成token
        serialize = Serialize(settings.SECRET_KEY, 3600)
        info = {'user_id':user.id}
        token = serialize.dumps(info)
        token = token.decode()
        msg = '<h1>欢迎您成为会员</h1><a href="http://127.0.0.1:8000/user/active/%s">请点击这里激活用户</a>'% (token)
        #发送激活邮件
        celery_task_send_mail.delay(user.email, msg)
        return redirect(reverse('user:login'))


class Login(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username':username, 'checked':checked})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')
        user = authenticate(username=username, password=password)
        next_url = request.GET.get('next', reverse('goods:index'))
        if user:
            login(request, user)
            response = redirect(next_url)
            if remember == 'on':
                response.set_cookie('username', username)
            else:
                response.delete_cookie('username')
            return response
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码不对'})


class Active_View(View):
    def get(self, request, token):
        #解密
        serialize = Serialize(settings.SECRET_KEY, 3600)
        try:
            token = serialize.loads(token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired:
            return HttpResponse('激活过期')

class User_Center(MixInClass, View):
    def get(self, request):
        user = request.user
        addr = Address.objects.get_address_defaul(user)
        conn = get_redis_connection(alias='default')
        history_key = 'history_%s'%user.id
        goods_list = conn.lrange(history_key, 0, 4)
        goods_li = []
        for id in goods_list:
            goods = GoodsSKU.objects.get(id = id)
            goods_li.append(goods)
        context = {'page':'user', 'addr':addr, 'goods_li':goods_li}
        return render(request, 'user_center_info.html', context)



class User_Order(MixInClass, View):
    def get(self, request):
        return render(request, 'user_center_order.html', {'page':'order'})

class User_Site(MixInClass, View):
    def get(self, request):
        user = request.user
        addr = Address.objects.get_address_defaul(user)
        return render(request, 'user_center_site.html', {'page':'site', 'addr':addr})
    def post(self, request):
        receiver = request.POST.get('receiver')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        addr = request.POST.get('addr')
        if not all([receiver, phone, addr]):
            return redirect(reverse('user:site'), {'errmsg':'输入的信息不完整'})
        if re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            user = request.user
            address = Address.objects.get_address_defaul(user)
            if address:
                is_default = False
            else:
                is_default = True
            Address.objects.create(receiver = receiver,
                                   phone = phone,
                                   zip_code = zip_code,
                                   is_default = is_default,
                                   user = user,
                                   addr = addr)
            return redirect(reverse('user:site'))
        else:
            return redirect(reverse('user:site'), {'errmsg': '手机号输入格式不对'})

class User_Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))




