""" File that keeps track of Django signals for Self.

Notes:
    Check out documentation here: 
    https://docs.djangoproject.com/en/3.1/topics/signals/
"""

from django.contrib.auth.models import Group


def create_groups(*args, **kwargs):
    """ Creates groups that can be given special permissions. """

    Group.objects.get_or_create(name="Owner")
    Group.objects.get_or_create(name="Admin")
    Group.objects.get_or_create(name="Moderator")
    Group.objects.get_or_create(name="User")
    Group.objects.get_or_create(name="Shadowed")
    Group.objects.get_or_create(name="Banned")
