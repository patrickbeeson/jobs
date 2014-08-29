# The Variable jobs app ReadME

va_jobs is a simple Django app to allow postings of job openings and acceptance of applications for those jobs.

## Quick start

1.  Add "jobs" to your `INSTALLED_APPS` setting like this:
    `INSTALLED_APPS = (
        ...
        'jobs',
    )`
2.  Include the jobs URLconf in your project urls.py like this: `url(r'^jobs/', include('jobs.urls')),`
3.  Run `python manage.py syncdb` to create the jobs models.
4.  Start the development server and visit http://127.0.0.1:8000/admin/ to create a job (you'll need the Admin app enabled).
5.  Visit http://127.0.0.1:8000/ to see the list of jobs. You can apply for a job from its detail view.