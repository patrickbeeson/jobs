from __future__ import absolute_import

from django.views.generic import TemplateView

from jobs.models import Job


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['jobs_list'] = Job.active.all()
        return context
