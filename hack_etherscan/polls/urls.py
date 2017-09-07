from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_tokens_from_view_tokentxns_page, name='get_tokens_from_view_tokens_page'),
]