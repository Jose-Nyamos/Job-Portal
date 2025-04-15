from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
from .models import *
import logging
from django.shortcuts import render, get_object_or_404
from django.urls import resolve


logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            if not UserProfile.objects.filter(user=user).exists():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                messages.warning(request, "User profile already exists.")

            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect_user_by_role(request, user)  # ✅ Pass both `request` and `user`

            messages.success(request, "Registration successful.")
            return redirect('login')

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'user/register.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def admin_dashboard(request):
    """Displays job postings, applicants' applications, and allows job posting and application approval."""
    # Fetch all job applications
    job_applications = JobApplication.objects.select_related('job', 'applicant').all()
    
    # Fetch all jobs posted by the admin
    posted_jobs = Job.objects.all()
    
    # Process new job posting form submission
    if request.method == 'POST' and 'post_job' in request.POST:
        job_form = JobForm(request.POST, request.FILES)  # Include files if logo is included
        if job_form.is_valid():
            job_form.save()  # Save the new job posting
            messages.success(request, "Job posted successfully.")
            return redirect('admin_dashboard')  # Redirect to the dashboard to view the posted job
        else:
            messages.error(request, "There was an error posting the job.")
    else:
        job_form = JobForm()  # Initialize empty form for posting job

    return render(request, 'user/admin-dashboard.html', {
        'job_applications': job_applications,
        'posted_jobs': posted_jobs,
        'job_form': job_form,
    })

@login_required
def applicant_dashboard(request):
    return render(request, 'user/applicant-dashboard.html')



def redirect_user_by_role(request, user):
    """Redirects user based on their role while preventing infinite loops."""
    try:
        role = user.userprofile.role
    except UserProfile.DoesNotExist:
        role = 'applicant'  # Default role if no profile exists

    # Get the current URL name to prevent redirect loops
    current_url = resolve(request.path_info).url_name  

    if role == 'admin' and current_url != 'admin_dashboard':  # Only redirect if not already on admin dashboard
        logger.info(f"Redirecting admin {user.username} to admin_dashboard")
        return redirect('admin_dashboard')  
    elif role == 'applicant' and current_url != 'applicant_dashboard':  # Only redirect if not already on applicant dashboard
        logger.info(f"Redirecting applicant {user.username} to applicant_dashboard")
        return redirect('applicant_dashboard')

    # If the user is on their designated dashboard, do nothing
    logger.info(f"Redirecting {user.username} to default dashboard")
    return redirect('dashboard')



def user_login(request):
    """Handles user login and redirects based on role"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect_user_by_role(request, user)  # ✅ Fix: Pass `request` and `user`

    form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})




@login_required
def dashboard(request):
    """Handles role-based dashboard views"""
    return redirect_user_by_role(request, request.user)

@login_required
def user_profile(request):
        """Displays and updates the user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('user_profile')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = UserProfileForm(instance=profile)

        # Select the correct dashboard template based on user type
        if request.user.is_superuser:
            dashboard_template = 'user/admin-dashboard.html'
        else:
            dashboard_template = 'user/applicant-dashboard.html'

        return render(request, 'user/profile.html', {
            'form': form,
            'dashboard_template': dashboard_template,
            'user': request.user,  # optional if not passed by default
        })


def user_logout(request):
    """Logs out the user and redirects to the login page"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def job_landing_page(request):
    jobs = Job.objects.all().order_by('-posted_at')[:5]  # Show latest 5 jobs
    return render(request, 'job/landing_page.html', {'jobs': jobs})


@login_required
def create_job_advertisement(request):
    """Allows admin to create a job advertisement."""
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Job advertisement created successfully!")
            return redirect('job_list')  # Redirect to the job list page after creation
    else:
        form = JobForm()

    return render(request, 'user/create_job_advertisement.html', {'form': form})

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')  # Fetch all jobs, sorted by latest first
    return render(request, 'job/job_list.html', {'jobs': jobs})

@login_required
def applicant_job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')  # Fetch all jobs, sorted by latest first
    return render(request, 'job/applicant_job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job:
        print(f"You clicked on job with ID: {job.id}")  # Debugging
    return render(request, 'job/job_detail.html', {'job': job})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != 'applicant':  # Only applicants can apply
        messages.error(request, "Only applicants can apply for jobs.")
        return redirect('applicant_job_list')

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('applicant_job_list')
    else:
        form = JobApplicationForm()

    return render(request, 'job/apply_job.html', {
        'form': form, 
        'job': job,
        'user_profile': user_profile,  # Pass user_profile details
    })

@login_required
def review_applications(request):
    """Allows admin to review job applications."""
    if not request.user.userprofile.role == 'admin':  # Only admins can access this
        messages.error(request, "You do not have permission to review applications.")
        return redirect('job_list')

    applications = JobApplication.objects.filter(status='pending')  # Show only pending applications
    return render(request, 'user/review_applications.html', {'applications': applications})



@login_required
def approve_application(request, application_id):
    """Allows admin to approve job applications."""
    if not request.user.userprofile.role == 'admin':  # Only admins can approve
        messages.error(request, "You do not have permission to approve applications.")
        return redirect('job_list')

    application = get_object_or_404(JobApplication, id=application_id)
    application.status = 'approved'
    application.approved_by = request.user
    application.save()

    messages.success(request, f"Application for {application.applicant.username} has been approved.")
    return redirect('review_applications')  # Redirect to review applications after approval


@login_required
def reject_application(request, application_id):
    """Allows admin to reject job applications."""
    if not request.user.userprofile.role == 'admin':  # Only admins can reject
        messages.error(request, "You do not have permission to reject applications.")
        return redirect('job_list')

    application = get_object_or_404(JobApplication, id=application_id)
    application.status = 'rejected'
    application.approved_by = request.user
    application.save()

    messages.error(request, f"Application for {application.applicant.username} has been rejected.")
    return redirect('review_applications')  # Redirect to review applications after rejection


@login_required
def applied_jobs(request):
    """Displays jobs the logged-in applicant has applied to."""
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'job/applied_jobs.html', {'applications': applications})




