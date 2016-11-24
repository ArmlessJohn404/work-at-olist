from django.conf.urls import url, include
from django.contrib import admin
from api.views import root_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^$', root_view),
]
