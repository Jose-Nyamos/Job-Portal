# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile when a new User is created."""
    if created:
        # Set the role based on whether the user is an admin or not
        if instance.is_superuser:
            role = 'admin'
        else:
            role = 'applicant'

        UserProfile.objects.create(user=instance, role=role)
        print(f"UserProfile created for {instance.username}, with role {role}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Saves the associated UserProfile whenever the User is saved."""
    try:
        instance.userprofile.save()
        print(f"UserProfile saved for user: {instance.username}")
    except UserProfile.DoesNotExist:
        print(f"UserProfile does not exist for user: {instance.username}")
