from django.urls import path, register_converter

from .converters import UrlKeyConverter
from .views import UrlRedirectView, ShortenUrlView, ListShortenUrlView


register_converter(UrlKeyConverter, 'uk')

urlpatterns = [
    path('api/shorten/', ShortenUrlView.as_view(), name='shorten'),
    path('api/shortens/', ListShortenUrlView.as_view(), name='shorten_list'),
    path('<uk:url_key>/', UrlRedirectView.as_view(), name='url_to_redirect'),
]
