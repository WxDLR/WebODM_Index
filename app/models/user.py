from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django import forms
from uuid import uuid4


class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_field):
        extra_field.setdefault('is_staff', False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_field)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid4)
    username = models.CharField(max_length=40, null=False, unique=True)
    phone_number = models.CharField(max_length=11, )
    email = models.EmailField()
    icon = models.ImageField()

    is_staff = models.BooleanField(
        # _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        # _('active'),
        default=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email', 'icon']

    objects = MyUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        db_table = "myuser"


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="name", required=True, max_length=16, min_length=6, help_text="Enter your name",
                           widget=forms.TextInput(attrs={"style": "text_alien:center"}))
    password = forms.CharField(label="password", required=True, min_length=6, widget=forms.PasswordInput())
    phone_number = forms.CharField(label="phone_number", required=False, max_length=11, min_length=11,
                                   help_text="Enter your name")
    email = forms.EmailField(label="email", required=True, error_messages={'required': "Email must not be empty",
                                                                           'invalid': "The form is invalid"})

    class Meta:
        model = MyUser
        fields = ("username", "password", "phone_number", "email")


class UserLoginForm(forms.Form):
    username = forms.CharField(label="name", required=True, max_length=16, min_length=6, help_text="Enter your name",
                           widget=forms.TextInput(attrs={"style": "text_alien:center"}))
    password = forms.CharField(label="password", required=True, min_length=6, widget=forms.PasswordInput())

    # class Meta:
    #     model = MyUser
    #     fields = ("name", "password")

