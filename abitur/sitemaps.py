from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        datet = obj.date_pub
        return datet


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['bakPage_url', 'interPage_url', 'infoPage_url', 'news_list_url', 'order_bak_url',
                'rec_list_bak_url', 'submit_doc_bak_url', 'order_mag_url', 'rec_list_mag_url',
                'submit_doc_mag_url', 'order_asp_url', 'rec_list_asp_url', 'submit_doc_asp_url',
                'mag_page_url', 'asp_page_url', 'infoOVZ_page_url', 'bak_calendar_url', 'result_bak_url',
                'result_mag_url', 'result_asp_url']

    def location(self, item):
        return reverse(item)
