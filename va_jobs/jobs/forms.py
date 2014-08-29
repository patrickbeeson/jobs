from django.forms import ModelForm

from .models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = [
            'first_name',
            'last_name',
            'email_address',
            'phone_number',
            'salary_requirement',
            'resume',
            'portfolio_url',
            'description',
            'can_relocate',
            'start_date',
        ]

    def clean(self):
        # Only allow certain file types for upload
        cleaned_data = super(ApplicationForm, self).clean()
        if cleaned_data.get('resume'):
            resume = cleaned_data.get('resume')
            resume_ext = resume.name.lower().split('.')[1]
            if not resume_ext in ('pdf', 'doc', 'docx'):
                del cleaned_data["resume"]
                msg = u"Your file must be a PDF or DOC file type."
                self._errors["resume"] = self.error_class([msg])
            return cleaned_data
        else:
            return cleaned_data
