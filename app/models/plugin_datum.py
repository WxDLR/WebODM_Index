import logging
from django.db import models
from django.contrib.postgres import fields
from django.contrib.auth.models import User
from .user import MyUser
logger = logging.getLogger('app.logger')


class PluginDatum(models.Model):
    key = models.CharField(max_length=255, help_text="Setting key", db_index=True)
    user = models.ForeignKey(MyUser, null=True, default=None, on_delete=models.CASCADE, help_text="The user this setting belongs to. If NULL, the setting is global.")
    int_value = models.IntegerField(blank=True, null=True, default=None, help_text="Integer value")
    float_value = models.FloatField(blank=True, null=True, default=None, help_text="Float value")
    bool_value = models.NullBooleanField(blank=True, null=True, default=None, help_text="Bool value")
    string_value = models.TextField(blank=True, null=True, default=None, help_text="String value")
    json_value = fields.JSONField(default=None, blank=True, null=True, help_text="JSON value")

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "插件"
        verbose_name_plural = verbose_name
