from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import re


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone_number(number):
    pattern = r'^\+7\d{10}$'
    return re.match(pattern, number) is not None


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if is_valid_email(username):
            user = UserModel.objects.filter(email=username).first()
        elif is_valid_phone_number(username):
            user = UserModel.objects.filter(profile__phone_number=username).first()
        else:
            user = UserModel.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None




