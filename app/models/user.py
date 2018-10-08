from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True, )

    name = models.CharField(max_length=40, null=False, unique=True)
    password = models.CharField(max_length=128, null=False)
    nickname = models.CharField(max_length=40, unique=True)
    phone_number = models.IntegerField()
    email = models.EmailField()
    icon = models.ImageField()

    def __str__(self):
        return "User"

    class Meta:
        db_table = "user"

