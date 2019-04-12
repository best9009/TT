from django.contrib import admin
from .models import GoodsType,IndexPromotionBanner, IndexTypeGoodsBanner, IndexGoodsBanner, GoodsImage, Goods, GoodsSKU
from celery_task.task import static_index_html_load


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        static_index_html_load.delay()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        static_index_html_load.delay()

class IndexTypeGoodsBannerAdmin(BaseAdmin):
    pass

class IndexGoodsBannerAdmin(BaseAdmin):
    pass
class GoodsSKUAdmin(BaseAdmin):
    pass
class GoodsTypeAdmin(BaseAdmin):
    pass
class GoodsImageAdmin(BaseAdmin):
    pass
class GoodsAdmin(BaseAdmin):
    pass


admin.site.register(IndexPromotionBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(Goods, GoodsAdmin)
#
# admin.site.register(IndexPromotionBanner)
# admin.site.register(IndexTypeGoodsBanner)
# admin.site.register(IndexGoodsBanner)
# admin.site.register(GoodsSKU)
# admin.site.register(GoodsType)
# admin.site.register(GoodsImage)
# admin.site.register(Goods)


