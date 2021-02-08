from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('receipt_home.urls',namespace="receipt_home")),
    path('favicon.png', RedirectView.as_view(url=staticfiles_storage.url('favicon.png'))),
    path("accounts/", include('accounts.urls', namespace="accounts")),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
# notify_user(repeat=10, repeat_until=None)