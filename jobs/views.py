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


logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)  # Ensure to include files if profile has file fields like image or resume

        if user_form.is_valid() and profile_form.is_valid():
            # Create user instance
            user = user_form.save()

            # Create associated profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Log the user in
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

            messages.success(request, "Registration successful.")
            return redirect('login')  # Redirect to a dashboard or home page after successful registration
        else:
            # If there are errors, add them to the message system
            if user_form.errors:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")

            if profile_form.errors:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'user/register.html', {'user_form': user_form, 'profile_form': profile_form})

def redirect_user_by_role(user):
    """Redirects user based on their role"""
    if user.is_superuser:
        logger.info(f"Redirecting superuser {user.username} to admin_dashboard")
        return redirect('admin_dashboard')
    elif user.is_staff:
        logger.info(f"Redirecting staff user {user.username} to dashboard")
        return redirect('dashboard')
    else:
        logger.info(f"Redirecting regular user {user.username} to applicant_dashboard")
        return redirect('applicant_dashboard')

def user_login(request):
    """Handles user login and redirects based on role"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User {user.username} authenticated successfully")
                return redirect_user_by_role(user)  # Redirect based on role
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                logger.warning(f"Authentication failed for user {username}")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                logger.warning(f"Form error: {error}")
    
    form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def dashboard(request):
    """Handles role-based dashboard views"""
    context = {
        'user': request.user
    }
    return render(request, 'user/dashboard.html', context)

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

    return render(request, 'user/profile.html', {'form': form})

def user_logout(request):
    """Logs out the user and redirects to the login page"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def job_landing_page(request):
    jobs = Job.objects.all().order_by('-posted_at')[:5]  # Show latest 5 jobs
    return render(request, 'job/landing_page.html', {'jobs': jobs})


# @login_required
def create_job_advertisement(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_job_advertisement')  # Redirect to a success page or list of jobs
    else:
        form = JobForm()
        
     # Fetch all jobs from the database
    jobs = Job.objects.all().order_by('-posted_at')  # Sort by latest jobs first

    return render(request, 'user/create_job_advertisement.html', {'form': form})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job:
        print(f"You clicked on job with ID: {job.id}")  # Debugging
    return render(request, 'job/job_detail.html', {'job': job})


