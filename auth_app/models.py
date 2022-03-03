from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

from django.db import models


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, ic, password=None, **extra_fields):
        """Create and save a User with the given ic and password."""
        if not ic:
            raise ValueError('The given ic must be set')
        user = self.model(ic=ic, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, ic, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(ic, password, **extra_fields)

    def create_superuser(self, ic, password=None, **extra_fields):
        """Create and save a SuperUser with the given ic and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(ic, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    
    username = None
    ic = CharField(max_length=12, unique=True, verbose_name='IC Number', blank=False,
                   help_text='Enter 12 digits ic number')

    USERNAME_FIELD = 'ic'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + self.last_name
    
    class Meta:
        db_table = 'auth_user'
