from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from . import views


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^user/(\d+)', views.single_user, name='single_user'),
    url(r'^profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)