""" Configuration for the selfauth client. """

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SelfConfig(AppConfig):
    name = "selfauth"
    verbose_name = "Self OpenID Auth"

    def ready(self):
        """Executes when the Django application is ready.

        Notes:
            We must import the signals through here due to Django's
            loading sequence. This ensures all apps are loaded before
            hand.
        """

        from . import signals

        post_migrate.connect(signals.create_groups, sender=self)
