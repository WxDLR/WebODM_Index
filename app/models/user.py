from django.db import models
from django import forms
from uuid import uuid4


class MyUser(models.Model):
    id = models.CharField(primary_key=True, max_length=128, default=uuid4, editable=False)
    username = models.CharField(max_length=40, null=False, unique=True)
    password = models.CharField(max_length=128, )
    phone_number = models.CharField(max_length=11, )
    email = models.EmailField()
    icon = models.ImageField()

    is_active = models.BooleanField(
        # _('active'),
        default=True,
    )
    # To Do
    # to active the user

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


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


