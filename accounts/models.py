from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField('Пароль', max_length=255)
    activation_code = models.CharField('Код активации', max_length=255, blank=True)
    password_reset_code = models.CharField('Код восстановления пароля', max_length=255, blank=True)
    username = models.CharField('username', max_length=100, blank=True)
    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self):
        self.activation_code = str(uuid4())

    def create_password_reset_code(self):
        from random import randint
        self.password_reset_code = str(randint(100000, 999999))
