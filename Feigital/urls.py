from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from feigitalApp.views import home

urlpatterns = [
    path('', home),
    path('produtos/', include('feigitalApp.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)