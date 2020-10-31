from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from book_store.utils import generate_slug


class UserCustomManager(BaseUserManager):
    """
    Custom user manager model
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        user.slug = generate_slug('user' + str(user.pk))
        user.authentication_key = generate_slug('user' + str(user.pk))
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserCustomManager()
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, auto_created=True, editable=False)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admins site.'),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admins site.'),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether this user has verified email/mobile. '

        ),
    )
    creation_timestamp = models.DateTimeField(_('Creation timestamp'), null=True, blank=True,
                                              auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name="user_create_by_rel", null=True,
                                   blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.get_full_name())

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        else:
            full_name = '%s' % self.first_name
        return full_name.strip()
