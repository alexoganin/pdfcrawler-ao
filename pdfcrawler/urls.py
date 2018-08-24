from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views
from . import settings

urlpatterns = [
    url(r'^$', views.index, name='main'),
    url(r'^crawler/', include('crawler.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
