from __future__ import absolute_import

from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns("",
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=views.JobDetailView.as_view(),
        name='job_detail'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/apply/$',
        view=views.ApplicationCreateView.as_view(),
        name='application_create'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/apply/submitted/$',
        view=TemplateView.as_view(template_name="jobs/application_submitted.html"),
    ),
)
