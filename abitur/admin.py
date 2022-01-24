from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'img', 'date']
    fields = ['title', 'body', 'img', 'date']

#регистрируем модели БД в админпанели
admin.site.register(News, NewsAdmin)
admin.site.register(NewsFile)
admin.site.register(Orders)
admin.site.register(OrdersSpec)
admin.site.register(RecommendedList)
admin.site.register(OrdersMag)
admin.site.register(RecommendedListMag)
admin.site.register(OrdersAsp)
admin.site.register(RecommendedListAsp)
admin.site.register(Result)
admin.site.register(ResultAsp)
admin.site.register(ResultMag)
