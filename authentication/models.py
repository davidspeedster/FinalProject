from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
import uuid
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, password, role):
        if not user_name:
            raise ValueError(_('You must provide a user name'))
        if not email:
            raise ValueError(_('You must provide an email address'))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, user_name=user_name, role=role)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"
    LAB_TECHNICIAN = "lab_technician"

    ROLE_CHOICES = (
        (DOCTOR, "doctor"),
        (RECEPTIONIST, "receptionist"),
        (LAB_TECHNICIAN, "lab_technician"),
    )
    uid = models.UUIDField(unique=True, editable=False,
                           default=uuid.uuid4, primary_key=True, verbose_name='Public identifier')
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True, null=True)
    role = models.CharField(max_length=150, null=True, choices=ROLE_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
