import csv
from dataclasses import asdict
from itertools import chain
from typing import List

from apps.utils import generate_key
from django.contrib import admin
from django.http import StreamingHttpResponse
from django.urls import path

from .data_models import UrlRow
from .export import Echo, UrlFields
from .mixins import BaseImportMixin
from .models import Url


@admin.register(Url)
class UrlAdmin(BaseImportMixin, admin.ModelAdmin):
    list_display = [
        'url_key', 'key', 'tag', 'usage_count', 'redirect_url',
        'shortened_url', 'created_at'
    ]
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

    def get_urls(self):
        urls = super().get_urls()
        info = self.get_model_info()
        my_urls = [
            path(
                'export-urls/',
                self.admin_site.admin_view(self.export_csv_view),
                name='%s_%s_export_csv' % info
            )
        ]

        return my_urls + urls

    def export_csv_view(self, request, *args, **kwargs):
        qs = Url.objects.all()
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        headers = {
            'Content-Disposition': 'attachment; filename="shortened-urls.csv"'
        }
        return StreamingHttpResponse(
            (
                writer.writerow((
                    r.redirect_url, r.url_key, r.key, r.tag, r.usage_count,
                    r.shortened_url, r.created_at
                ))
                for r in chain((UrlFields(),), qs)
            ),
            content_type='text/csv',
            headers=headers,
        )
