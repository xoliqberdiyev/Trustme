from django.contrib.auth.models import UserManager 
from django.contrib.auth.hashers import make_password


class BaseUserManager(UserManager):
    def _create_user_object(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone must be set")
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone, password, **extra_fields):
        user = self._create_user_object(phone, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)
