""" Custom user management system that integrates Self. """

import random

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ROLES = [
    ("Owner", "Owner"),
    ("Admin", "Admin"),
    ("Moderator", "Moderator"),
    ("User", "User"),
    ("Shadowed", "Shadowed"),
    ("Banned", "Banned"),
]


def generate_sub():
    """Generates an 64-byte long hexadecimal unique ID. Used for the user."""

    return hex(random.getrandbits(256))[2:]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, **kwargs):
        """Create and save a user with the given username, email, and password.

        Note:
            Password for Self's users are not saved, and are kept empty.
        """

        if not username or not email:
            raise ValueError("A valid email and username are needed.")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **kwargs)
        user.set_unusable_password()
        user.save(using=self._db)

        # Creates entry in the 'allauth' implementation of 'EmailAddress'.
        UserEmail.objects.create(user=user, email=email, primary=True, verified=False)

        return user


class User(AbstractUser):
    """Custom user model class that integrates with all of Self's scopes.

    Notes:
        Subject identifier (sub) is required to create a user, and must
        always be unique; it defaults in case user is registering without
        Self.
    """

    sub = models.CharField(
        verbose_name="Subject Identifier",
        max_length=64,
        editable=False,
        default=generate_sub,
        primary_key=True,
    )
    first_name = models.CharField("First Name", max_length=30, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=150, blank=True, null=True)
    gender = models.TextField(verbose_name="Gender", blank=True, null=True)
    birthday = models.DateField(verbose_name="Birthday", blank=True, null=True)

    objects = CustomUserManager()


class UserEmail(models.Model):
    """ One-to-many relationship between user and email. """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    primary = models.BooleanField(verbose_name="Primary", default=False)
    email = models.EmailField(verbose_name="E-Mail Address")
    verified = models.BooleanField(verbose_name="Verified", default=False)


class UserAddress(models.Model):
    """ One-to-many relationship between user and address. """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    primary = models.BooleanField(verbose_name="Primary Address", default=False)
    country = models.CharField(verbose_name="Country", max_length=250, blank=True)
    state = models.CharField(verbose_name="State", max_length=250, blank=True)
    city = models.CharField(verbose_name="City", max_length=250, blank=True)
    address1 = models.CharField(verbose_name="Address One", max_length=250, blank=True)
    address2 = models.CharField(verbose_name="Address Two", max_length=250, blank=True)
    zipcode = models.CharField(verbose_name="Zip Code", max_length=250, blank=True)

    def get_full_address(self):
        return f"{self.address1}, {self.address2}, {self.city} {self.state}, {self.country}"

    def get_street_address(self):
        return f"{self.address1}, {self.address2}"


class UserPhone(models.Model):
    """ One-to-many relationship between user and phone numbers. """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    primary = models.BooleanField(verbose_name="Primary Phone Number", default=False)
    number = PhoneNumberField(verbose_name="Phone Number", unique=True)
    verified = models.BooleanField(verbose_name="Phone Number Verified", default=False)


class UserAvatar(models.Model):
    """One-to-many relationship between user and avatar."""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    primary = models.BooleanField(verbose_name="Primary Avatar", default=False)
    url = models.TextField(verbose_name="Avatar URL")


class UserSocial(models.Model):
    """One-to-many relationship between user and avatar.

    Notes:
        This is only used internally at Column. External apps do
        not have access to the necessary scope permissions to access
        this information.
    """

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token = models.CharField(verbose_name="Token", max_length=1024)
    token_secret = models.CharField(verbose_name="Token Secret", max_length=1024)
    expires_at = models.DateField(verbose_name="Expiration Date")


class UserSetting(models.Model):
    """ One-to-one relationship betweem user and settings. """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default="User")
