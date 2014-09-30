from __future__ import absolute_import
import pytz
import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.utils.timezone import utc

from .models import Job, Application
from .forms import ApplicationForm


class JobDetailView(DetailView):
    model = Job


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    success_url = 'submitted/'

    def dispatch(self, *args, **kwargs):
        self.job = get_object_or_404(Job, slug=kwargs['slug'])
        return super(ApplicationCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #Get associated job and save
        self.object = form.save(commit=False)
        self.object.job = self.job
        self.object.save()

        # Gather cleaned data for email send
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email_address = form.cleaned_data.get('email_address')
        phone_number = form.cleaned_data.get('phone_number')
        salary_requirement = form.cleaned_data.get('salary_requirement')
        description = form.cleaned_data.get('description')
        portfolio_url = form.cleaned_data.get('portfolio_url')
        can_relocate = form.cleaned_data.get('can_relocate')
        start_date = form.cleaned_data.get('start_date')
        resume = self.object.resume
        job = self.object.job

        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        est = pytz.timezone('US/Eastern')
        submission_date = now.astimezone(est).strftime('%A, %B %d %Y, %I:%M %p')

        #Compose message
        email = EmailMessage()
        email.body = 'Name: ' + first_name + last_name + '\n' + 'Email: ' + email_address + '\n' + 'Phone number: ' + str(phone_number) + '\n' + 'Salary requirement: ' + str(salary_requirement) + '\n' + 'Description: ' + description + '\n' + 'Portfolio URL: ' + portfolio_url + '\n' + 'Can relocate: ' + str(can_relocate) + '\n' + 'Start date: ' + str(start_date)
        email.subject = 'A new application has been submitted {submission_date} for {job}'.format(submission_date=submission_date, job=job)
        email.from_email = 'noreply@mail.thevariable.com'
        email.to = ['jobs@thevariable.com']
        email.bcc = ['admin@jobs.thevariable.com']
        email.attach(resume.name, resume.read())
        email.send()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ApplicationCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({'job': self.job})
        return context_data
