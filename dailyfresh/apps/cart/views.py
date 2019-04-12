from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from util.mixin import MixInClass
from goods.models import GoodsSKU

class AddCartView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1, 'msg':'请先登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        count = int(count)
        conn = get_redis_connection('default')
        cart_key = 'cart_%s'%user.id
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)
        conn.hset(cart_key, sku_id, count)
        total_count = conn.hlen(cart_key)
        return JsonResponse({'res':3, 'total_count':total_count, 'msg':'添加成功'})

class CartView(MixInClass, View):
    def get(self, request):
        user = request.user
        cart_key = 'cart_%s'%user.id
        conn = get_redis_connection('default')
        cart_dict = conn.hgetall(cart_key)
        total_price = 0;
        total_count = 0
        skus = []
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            amount = sku.price*int(count)
            sku.count = count
            sku.amount = amount
            total_count += int(count)
            total_price += amount
            skus.append(sku)
        context = {'skus' : skus,
                   'total_price' : total_price,
                   'total_count' : total_count}
        return render(request, 'cart.html', context)

class CartUpdateView(View):
    def post(self, request):
        sku_id = request.POST.get('sku_id')
        count = int(request.POST.get('count'))
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res':1, 'msg':'用户未登录'})
        cart_key = 'cart_%s'%user.id
        conn = get_redis_connection('default')
        conn.hset(cart_key, sku_id, count)
        #vals = conn.hvals
        return  JsonResponse({'res':2, 'msg':'修改成功'})

class CartDelView(View):
    def post(self, request):
        user = request.user
        sku_id = request.POST.get('sku_id')
        cart_key = 'cart_%s'%user.id
        conn = get_redis_connection()
        conn.hdel(cart_key, sku_id)
        return JsonResponse({'res' : 1, 'msg' : '删除成功'})
