from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from oscar.apps.customer.abstract_models import AbstractUser


class UserManager(auth_models.BaseUserManager):

    def create_user(self, phone_number ,password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not phone_number:
            raise ValueError('The given phone_number must be set')
        # phone_number = phone_number
        user = self.model(
            phone_number=phone_number, is_staff=False, is_active=True,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        u = self.create_user(phone_number, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(AbstractUser):
    phone_number = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True)
    email = None

    object = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name.upper(), self.first_name)
        return full_name.strip()

    def get_username(self) -> str:
        username = self.first_name +' ' + self.last_name
        return username
