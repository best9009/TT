from django.shortcuts import render, redirect
from django.views.generic import View
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner,GoodsSKU
from django_redis import get_redis_connection
from orders.models import OrderGoods
from django.core.paginator import Paginator

class Index(View):
    def get(self, request):
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
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            con = get_redis_connection()
            cart_key = 'cart_%s'%user.id
            cart_count = con.hlen(cart_key)
        context = {'types':types,
                   'index_goods_banner':index_goods_banner,
                   'index_promotion_banner':index_promotion_banner,
                   'cart_count':cart_count}
        return render(request, 'index.html', context)

class DetailView(View):
    def get(self, request, goods_id):
        types = GoodsType.objects.all()
        goods_sku = GoodsSKU.objects.get(id=goods_id)

        loc_type = goods_sku.type

        goods = goods_sku.goods
        #订单
        order_goods = OrderGoods.objects.filter(sku=goods_sku).exclude(comment='')
        new_goods = GoodsSKU.objects.filter(type=loc_type).order_by('-create_time')[:2]
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            conn = get_redis_connection('default')
            cart_key = 'cart_%s'%user.id
            cart_count = conn.hlen(cart_key)
        context = {'types':types,
                   'goods_sku': goods_sku,
                   'loc_type' : loc_type,
                   'goods' : goods,
                   'order_goods' : order_goods,
                   'new_goods' : new_goods,
                   'cart_count' : cart_count}
        user = request.user
        if user.is_authenticated():
            conn = get_redis_connection('default')
            history_key = 'history_%s' % user.id
            conn.lrem(history_key, 0, goods_sku.id)
            conn.lpush(history_key, goods_sku.id)
            conn.ltrim(history_key, 0, 4)
        return render(request, 'detail.html', context)

class ListView(View):
    def get(self, request, type_id, page_num):
        #/list/1/1?sort=''
        #sort : default 默认 price 价格 hot 人气
        types = GoodsType.objects.all()
        sort = request.GET.get('sort')
        type = GoodsType.objects.get(id=type_id)
        new_type_goods = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('sales')
        else:
            skus = GoodsSKU.objects.filter(type=type).order_by('id')
            sort = 'default'
        page_num = int(page_num)
        pg = Paginator(skus, 2)
        page = pg.page(page_num)
        context = {'types':types,
                   'type':type,
                   'page_num':page_num,
                   'page':page,
                   'sort':sort,
                   'new_type_goods':new_type_goods,
                   'pg':pg}

        return  render(request, 'list.html', context)



