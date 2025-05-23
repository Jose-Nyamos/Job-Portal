from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Freelance', 'Freelance'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    posted_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='job_logos/', null=True, blank=True)  # New field for job logo

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('applicant', 'applicant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='applicant')  # Role selection
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to user
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover_letters/', null=True, blank=True, help_text="Upload your cover letter in PDF format.")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_applications')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title} ({self.status})"
