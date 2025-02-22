from django.shortcuts import render
from .models import Job


def job_landing_page(request):
    jobs = Job.objects.all().order_by('-posted_at')[:5]  # Show latest 5 jobs
    return render(request, 'job/landing_page.html', {'jobs': jobs})
