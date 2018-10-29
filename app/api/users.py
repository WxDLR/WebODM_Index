from app.models import user
from rest_framework import serializers
from rest_framework import viewsets


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user.MyUser
        fields = ('id', 'username', 'email', 'phone_number', 'icon')


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = user.MyUser.objects.all().order_by('id')
    serializer_class = MyUserSerializer
    ordering_fields = ('username',)

