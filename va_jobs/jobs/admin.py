from django.contrib import admin
from django.conf import settings

from .models import Job, Application


class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'posted_date', 'modified']
    list_filter = ['engagement_type', 'is_expired']


class ApplicationAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display_links = ['full_name', 'resume_download']
    list_display = [
        'full_name',
        'email_address',
        'phone_number',
        'job',
        'status',
        'submission_date',
        'resume_download'
    ]
    list_filter = [
        'can_relocate',
        'status',
        'submission_date'
    ]
    fieldsets = (
        ('Contact information', {
            'fields': (
                'first_name',
                'last_name',
                'email_address',
                'phone_number'
            )
        }),
        ('Application information', {
            'fields': (
                'job',
                'resume_download',
                'description',
                'salary_requirement',
                'start_date',
                'can_relocate',
                'portfolio',
            )
        }),
        ('Meta options', {
            'classes': ('collapse',),
            'fields': ('status', 'submission_date',)
        }),
    )
    readonly_fields = (
        'first_name',
        'last_name',
        'email_address',
        'phone_number',
        'salary_requirement',
        'resume_download',
        'portfolio',
        'description',
        'can_relocate',
        'start_date',
        'job',
        'submission_date'
    )

    def resume_download(self, obj):
        return '<a href="%s%s">Download resume</a>' % (settings.MEDIA_URL, obj.resume)
    resume_download.allow_tags = True

    def portfolio(self, obj):
        if obj.portfolio_url:
            return '<a href="%s">Visit portfolio website</a>' % (obj.portfolio_url)
    portfolio.allow_tags = True

admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
