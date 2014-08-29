from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from .forms import ApplicationForm
from .models import Job, Application
from .views import JobDetailView
from . import views


class JobTestModel(TestCase):

    def setUp(self):
        self.job = mommy.make(
            Job,
            slug='test-job'
        )

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('jobs_list' in response.context)
        self.assertEqual([job.pk for job in response.context['jobs_list']], [1])

    def text_detail(self):
        response = self.client.get(reverse('detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['job'].slug, 'test-job')

        response = self.client.get('/test-job-2/')
        self.assertEqual(self.status_code, 404)


class ApplicationTestModel(TestCase):

    def setUp(self):
        self.job = mommy.make(
            Job,
            slug='test-job'
        )
        self.applicant = mommy.make(
            'jobs.Application',
            phone_number='555-555-5555',
            job=self.job
        )

    def test_valid_form(self):
        application = mommy.make('jobs.Application', phone_number='555-555-5555')
        form = ApplicationForm(instance=application)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = mommy.make(Application, phone_number='555-555-5555')
        form = ApplicationForm(instance=data)
        self.assertFalse(form.is_valid())
