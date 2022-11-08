from django.urls import path

from .views import UrlRedirectView, ShortenUrlView, ListShortenUrlView

urlpatterns = [
    path('<str:url_key>/', UrlRedirectView.as_view(), name='url_to_redirect'),
    path('api/shorten/', ShortenUrlView.as_view(), name='shorten'),
    path('api/shortens/', ListShortenUrlView.as_view(), name='shorten_list'),
]
