import datetime
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc

from model_utils.models import TimeStampedModel
from model_utils.managers import QueryManager
from model_utils import Choices
from localflavor.us.models import PhoneNumberField
from south.modelsinspector import add_introspection_rules

now = datetime.datetime.utcnow().replace(tzinfo=utc)


# Customize the upload path to organize resumes by job
def get_upload_path(instance, filename):
    return os.path.join(
        "resumes/{year}/{month}/{day}/{job}/{resume}".format(
            year=instance.submission_date.strftime('%Y'),
            month=instance.submission_date.strftime('%b'),
            day=instance.submission_date.strftime('%d'),
            job=instance.job.slug,
            resume=filename
        )
    )


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
    is_expired = models.BooleanField(
        default=False,
        help_text='Check if the job has been filled. '
                  'Expired jobs will not be displayed to the public.'
    )
    portfolio_required = models.BooleanField(default=True)
    engagement_type = models.CharField(
        choices=ENGAGEMENT_TYPE_CHOICES,
        default=FULLTIME,
        max_length=2
    )

    objects = models.Manager()
    active = QueryManager(is_expired=False)

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
    STATUS = Choices(
        ('pursue', _('pursue')),
        ('decline', _('decline')),
        ('no_action_taken', _('no action taken'))
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField()
    phone_number = PhoneNumberField(help_text='Please use the format XXX-XXX-XXXX.')
    salary_requirement = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Please use numbers only.'
    )
    resume = models.FileField(
        upload_to=get_upload_path,
        help_text='Please upload .pdf, .doc or .docx files only.'
    )
    portfolio_url = models.URLField(blank=True)
    description = models.TextField(
        blank=True,
        help_text='Please use Markdown for formatting if needed. No HTML is allowed.'
    )
    can_relocate = models.NullBooleanField(
        default=True,
        blank=True,
        null=True
    )
    start_date = models.DateField(
        default=datetime.date.today,
        blank=True,
        null=True,
        help_text='When can you start? Please use the following format: mm/dd/yyyy'
    )
    job = models.ForeignKey(Job)
    submission_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        default=datetime.date.today
    )
    status = models.CharField(
        choices=STATUS,
        default=STATUS.no_action_taken,
        max_length=20
    )

    #To allow PhoneNumberField to work with South migration.
    add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    class Meta:
        verbose_name_plural = 'Applications'
        ordering = ('-submission_date',)

    def __unicode__(self):
        return self.full_name
