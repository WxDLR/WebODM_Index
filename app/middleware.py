from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from jwt import ExpiredSignatureError
from rest_framework_jwt.utils import jwt_decode_handler

from app.models.user import MyUser


def get_user(request):
    token = request.COOKIES.get("Okaygis", None)
    if token:
        try:
            payload = jwt_decode_handler(token)
            user_id = payload.get("user_id")
            user = MyUser.objects.get(id=user_id)
            return user
        except ExpiredSignatureError as e:
            return e


class MyUserAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            request.myuser = get_user(request)
        except ExpiredSignatureError:
            resp = HttpResponse(content="%s, Please login again" % (e,))
            resp.delete_cookie("Okaygis")
            return resp
