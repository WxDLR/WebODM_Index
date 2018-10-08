from django.db import models
from django import forms
from uuid import uuid4


class User(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid4)

    name = models.CharField(max_length=40, null=False, unique=True)
    password = models.CharField(max_length=128, null=False)
    nickname = models.CharField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=11, unique=True, )
    email = models.EmailField()
    icon = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "app_user"


class UserForms(forms.ModelForm):
    name = forms.CharField(label="name", required=True, max_length=16, min_length=6, help_text="Enter your name",
                           widget=forms.TextInput(attrs={"style": "text_alien:center"}))
    password = forms.CharField(label="password", required=True, min_length=6, widget=forms.PasswordInput())
    nickname = forms.CharField(label="nickname", max_length=16, min_length=6, help_text="Enter your nick name")
    phone_number = forms.CharField(label="phone_number", required=False, max_length=11, min_length=11,
                                   help_text="Enter your name")
    email = forms.EmailField(label="email", required=True, error_messages={'required': "Email must not be empty",
                                                                           'invalid': "The form is invalid"})

    class Meta:
        model = User
        fields = ("name", "nickname", "password", "phone_number", "email")


