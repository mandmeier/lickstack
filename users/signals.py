"""
this will automatically create a profile for a new user
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # create profile for that user


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):  # saves profile
    instance.profile.save()
