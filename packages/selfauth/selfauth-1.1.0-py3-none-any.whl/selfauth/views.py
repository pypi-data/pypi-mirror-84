""" View definitions for the application. Used for testing purposes only. """

from django.shortcuts import render
from django.views.generic import TemplateView

from .models import (
    UserEmail,
    UserAddress,
    UserPhone,
    UserSetting,
    UserAvatar,
    UserSocial,
)


class TestView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        """ A test page for selfauth. """

        if request.user.is_authenticated:
            context = {
                "emails": UserEmail.objects.filter(user=request.user),
                "avatars": UserAvatar.objects.filter(user=request.user),
                "addresses": UserAddress.objects.filter(user=request.user),
                "phones": UserPhone.objects.filter(user=request.user),
                "settings": UserSetting.objects.filter(user=request.user),
                "socials": UserSocial.objects.filter(user=request.user),
            }
        else:
            context = {}

        return render(request, self.template_name, context)
