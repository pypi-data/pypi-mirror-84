""" File that includes modifications to the mozilla-django-oidc module. """

import logging

from django.contrib.auth.models import Group
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from . import models

LOGGER = logging.getLogger(__name__)


class SelfAuthenticationBackend(OIDCAuthenticationBackend):
    def get_username(self, claims):
        """Returns the username of the user.

        Note:
            This is overwritten because 'create_user' utilizes this function.
            Not sure if any other function uses this, so we do it this way
            just in case.
        """

        return claims.get("preferred_username")

    def get_primary_email(self, claims):
        """ Returns the user's primary email. """

        emails = claims.get("emails")
        for email in emails:
            if email["primary"]:
                return email["email"]

    def create_user(self, claims):
        """Creates the user based on the passed claims.

        Note:
            This function needs to be overwritten because 'sub' is not included.

            This uses the custom UserModel that is created inside of 'model.py'.
        """

        sub = claims.get("sub")
        email = self.get_primary_email(claims)
        username = self.get_username(claims)

        return self.UserModel.objects.create_user(
            username=username,
            email=email,
            password=None,
            sub=sub,
        )

    def filter_users_by_claims(self, claims):
        """Gathers Meta user(s) that match the OAuth 2.0 claims passed.

        Note:
            This function needs to be overwritten because it is utilized by
            the function 'get_or_create_user` at the bottom of this file.

            The original method is to utilize 'email', but 'sub' gives a
            better mean to ensure the user is always unique in Self and
            Meta. 'sub' is "Subject Identifier," and is unique and static
            per user.
        """

        sub = claims.get("sub")
        if not sub:
            return self.UserModel.objects.none()
        else:
            return self.UserModel.objects.filter(sub=sub)

    def verify_claims(self, claims):
        """Verifies the claim settings; sets to defaults if settings not given.

        Note:
            This function needs to be overwritten because it is utilized by
            the function 'get_or_create_user` at the bottom of this file.

            The original method did not include profile as a default settings
            if the 'OIDC_RP_SCOPES' settings param was missing in settings.py.
        """

        scopes = self.get_settings("OIDC_RP_SCOPES", "openid profile email")

        # Returns false is we are not using OpenID Connect.
        if "openid" not in scopes:
            return False

        return True

    def update_user(self, user, claims):
        """Updates the user with new claims given by the server.

        Note:
            This function needs to be overwritten because it is utilized by
            the function 'get_or_create_user` at the bottom of this file.

            The original method would simply return the user, and never modify
            it. Updated so that user information is transfered between Self and
            Meta on every session update between both services.
        """

        # Updates user.
        user.email = self.get_primary_email(claims)
        user.username = claims.get("preferred_username")
        user.first_name = claims.get("given_name", None)
        user.last_name = claims.get("family_name", None)
        user.gender = claims.get("gender", None)
        user.birthday = claims.get("birthdate", None)

        user.save()

        # Updates avatars.
        models.UserAvatar.objects.filter(user=user).delete()
        for picture in claims.get("pictures", []):
            models.UserAvatar.objects.get_or_create(
                user=user,
                primary=picture["primary"],
                url=picture["avatar_url"],
            )

        # Updates email addresses.
        models.UserEmail.objects.filter(user=user).delete()
        for email in claims.get("emails", []):
            models.UserEmail.objects.get_or_create(
                user=user,
                email=email["email"],
                primary=email["primary"],
                verified=email["verified"],
            )

        # Updates phone numbers.
        models.UserPhone.objects.filter(user=user).delete()
        for phone in claims.get("phones", []):
            models.UserPhone.objects.get_or_create(
                user=user,
                number=f"+{phone['phone']['country_code']}{phone['phone']['number']}",
                primary=phone["primary"],
                verified=phone["verified"],
            )

        # Updates addresses.
        models.UserAddress.objects.filter(user=user).delete()
        for address in claims.get("addresses", []):
            models.UserAddress.objects.get_or_create(
                user=user,
                primary=address["primary"],
                country=address["country"],
                state=address["state"],
                city=address["city"],
                address1=address["address1"],
                address2=address["address2"],
                zipcode=address["zipcode"],
            )

        # Setting Update
        settings_scope = claims.get("setting", {})
        if settings_scope:
            Group.objects.get(name=settings_scope["role"])
            models.UserSetting.objects.get_or_create(user=user, **settings_scope)

            # Set staff status for Owner, Admin, and Moderator roles.
            if settings_scope["role"] in ("Owner", "Admin", "Moderator"):
                user.is_staff = True

                if settings_scope["role"] == "Owner":
                    user.is_superuser = True

            user.save()

        # Token update.
        models.UserSocial.objects.filter(user=user).delete()
        for social in claims.get("social", []):
            models.UserSocial.objects.get_or_create(
                user=user,
                token=social["token"],
                token_secret=social["token_secret"],
                expires_at=social["expires_at"],
            )

        return user

    def get_or_create_user(self, access_token, id_token, payload):
        """Gets or creates a user in the local database.

        Note:
            Returns a User instance if 1 user is found. Creates a user if not
            found and configured to do so. Returns nothing if multiple users
            are matched.
        """

        # Gets the user information from Self.
        user_info = self.get_userinfo(access_token, id_token, payload)

        # Verifies the scope/claim settings.
        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = "Your OIDC_RP_SCOPES settings must include 'openid' as a scope."
            raise SuspiciousOperation(msg)

        # Grabs users with the 'sub' passed by 'user_info'.
        users = self.filter_users_by_claims(user_info)

        if len(users) == 1:
            # If user already exists, just update his/her info and return it.
            return self.update_user(users[0], user_info)

        elif len(users) > 1:
            # Return error if there are multiple users with the same 'sub' tag.
            msg = "There are multiple users registered with the same unique subject identifier. Cannot procced."
            raise SuspiciousOperation(msg)

        elif self.get_settings("OIDC_CREATE_USER", True):
            # Create and populate user with info.
            user = self.create_user(user_info)
            self.update_user(user, user_info)
            return user

        else:
            # User was not created, neither found.
            sub = user_info.get("sub")
            username = user_info.get("preferred_username")
            email = user_info.get("email")

            LOGGER.debug(
                (
                    "Login failed: No user with the following information was found:",
                    f"   Username: {username}",
                    f"   Email: {email}",
                    f"   Subject Identifier: {sub}",
                ),
            )

            return None
