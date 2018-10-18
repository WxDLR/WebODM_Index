from rest_framework import serializers
from app.models.user import MyUser


class MyUserSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return instance.username
