from dataclasses import asdict
from typing import List
from django.contrib import admin

from apps.utils import generate_key
from .data_models import UrlRow
from .mixins import BaseImportMixin
from .models import Url


@admin.register(Url)
class UrlAdmin(BaseImportMixin, admin.ModelAdmin):
    list_display = ['url_key', 'key', 'tag', 'usage_count', 'redirect_url']
    list_display_links = list_display

    import_template_name = 'admin/shortener/import_urls.html'
    row_model = UrlRow

    @staticmethod
    def process_result(rows: List[UrlRow]):
        urls = list()
        for row in rows:
            data = asdict(row)
            data.pop('message', None)
            url_key = generate_key(url=row.redirect_url)
            url = Url.objects.filter(url_key=url_key).first()
            if url:
                url_key = generate_key(url=row.redirect_url, shuffle=True)

            urls.append(Url(url_key=url_key, **data))

        if urls:
            Url.objects.bulk_create(urls)
