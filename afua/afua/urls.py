
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static  # serve media files
from django.conf import settings

# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/',include('allauth.urls')),
]
urlpatterns += i18n_patterns()

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += format_suffix_patterns(urlpatterns)
