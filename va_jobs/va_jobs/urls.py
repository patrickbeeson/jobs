from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

from .views import HomePageView

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('jobs.urls', namespace='jobs')),

    url(r'^$', HomePageView.as_view(), name='home'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)