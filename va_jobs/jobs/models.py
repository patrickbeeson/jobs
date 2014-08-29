import datetime

from django.db import models

from model_utils.models import TimeStampedModel
from localflavor.us.models import PhoneNumberField
from south.modelsinspector import add_introspection_rules


class ActiveJobManager(models.Manager):
    """
    Manager to fetch jobs that are not expired.

    """
    def get_query_set(self):
        return super(ActiveJobManager, self).get_query_set().filter(is_expired=False)


class Job(TimeStampedModel):
    """
    A job opening.

    """
    FULLTIME = 'ft'
    PARTTIME = 'pt'
    CONTRACT = 'co'
    ENGAGEMENT_TYPE_CHOICES = (
        (FULLTIME, 'full time'),
        (PARTTIME, 'part time'),
        (CONTRACT, 'contract')
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(help_text='This field is populated from the title field.')
    description = models.TextField(help_text='Please use Markdown format.')
    requirements = models.TextField(help_text='Please use Markdown format.')
    posted_date = models.DateField()
    is_expired = models.BooleanField(default=False, help_text='Check if the job has been filled. Expired jobs will not be displayed to the public.')
    portfolio_required = models.BooleanField(default=True)
    engagement_type = models.CharField(choices=ENGAGEMENT_TYPE_CHOICES, default=FULLTIME, max_length=2)

    objects = models.Manager()
    active = ActiveJobManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ('-created',)
        verbose_name_plural = 'Jobs'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('jobs:detail',
                (),
                {'slug': self.slug})


class Application(models.Model):
    """
    An applicantion for a job.

    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField()
    phone_number = PhoneNumberField(help_text='Please use the format XXX-XXX-XXXX.')
    salary_requirement = models.PositiveIntegerField(blank=True, null=True, help_text='Please use numbers only.')
    resume = models.FileField(upload_to='resumes', help_text='Please upload .pdf, .doc or .docx files only.')
    portfolio_url = models.URLField(blank=True)
    description = models.TextField(blank=True, help_text='Please use Markdown for formatting if needed. No HTML is allowed.')
    can_relocate = models.NullBooleanField(default=True, blank=True, null=True)
    start_date = models.DateField(default=datetime.date.today, blank=True, null=True, help_text='When can you start? Please use the following format: mm/dd/yyyy')
    job = models.ForeignKey(Job)

    #To allow PhoneNumberField to work with South migration.
    add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    class Meta:
        verbose_name_plural = 'Applications'
        ordering = ('job',)

    def __unicode__(self):
        return self.full_name
