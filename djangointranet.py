from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib import admin

from intranet.urls import urlpatterns as intranet_urlpatterns

admin.autodiscover()

# Default URLs patterns from intranet
urlpatterns = intranet_urlpatterns

# Add specific patterns
urlpatterns += patterns('',

                url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),

                # Apps
                url(r'^prospect/', include('prospect.urls')),

                # Admin URLs
                url(r'^admin/', include(admin.site.urls)),
                url(r'^admin_tools/', include('admin_tools.urls')),

                )

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
