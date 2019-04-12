from django.shortcuts import render
from django.views.generic import View
from util.mixin import MixInClass
from django_redis import get_redis_connection
from goods.models import GoodsSKU
from users.models import Address
from django.db import transaction
from orders.models import OrderInfo,OrderGoods
from datetime import datetime
from django.http import JsonResponse

class OrderPayView(MixInClass, View):
    def post(self, request):
        user = request.user
        sku_ids = request.POST.getlist('sku_ids')
        conn = get_redis_connection('default')
        cart_key = 'cart_%s'%user.id
        trans_price = 10
        skus = []
        total_count = 0
        total_price = 0
        addrs = Address.objects.filter(user=user)
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = int(conn.hget(cart_key, sku_id))
            sku.count = count
            price = sku.price
            amount = count*price
            sku.amount = amount
            skus.append(sku)
            total_count += count
            total_price += amount
        total_pay = total_price+trans_price
        sku_ids = ','.join(sku_ids)
        context = {'skus':skus,
                   'addrs':addrs,
                   'trans_price':trans_price,
                   'total_count':total_count,
                   'total_price':total_price,
                   'sku_ids':sku_ids,
                   'total_pay':total_pay}
        return render(request, 'place_order.html', context)

class OrderCommitView(View):
    def post(self, request):
        addr_id = request.POST.get('addr_id')
        pay_style = request.POST.get('pay_style')
        sku_ids = request.POST.get('sku_ids')
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%s'%user.id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)
        addr = Address.objects.get(id=addr_id)
        #创建事物保存节点
        save_point = transaction.savepoint()
        total_count = 0
        total_price = 0
        order = OrderInfo.objects.create(order_id=order_id,
                                         user=user,
                                         addr=addr,
                                         pay_method=int(pay_style),
                                         transit_price=10,
                                         order_status=1,
                                         total_price=total_price,
                                         total_count=total_count)
        sku_ids = sku_ids.split(',')
        for sku_id in sku_ids:
            count = int(conn.hget(cart_key, sku_id))
            #加悲观所
            with transaction.atomic():
                sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                stock = sku.stock
                if(count>stock):
                    transaction.savepoint_rollback(save_point)
                    return JsonResponse({'res':1, 'msg':'库存不足'})
                price = sku.price
                total_count += count
                total_price += count*price
                OrderGoods.objects.create(order=order,
                                          sku=sku,
                                          count=count,
                                          price=price,
                                          )
                sku.stock = stock-count
                sku.sales += count
                sku.save()

        order.total_price = total_price
        order.total_count = total_count
        order.save()

        transaction.savepoint_commit(save_point)
        #删除购物车中对应的条目
        conn.hdel(cart_key, *sku_ids)
        return  JsonResponse({'res':2, 'msg':'订单创建成功'})