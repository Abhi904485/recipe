"""Database Models"""

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.db import models


class UserManager(BaseUserManager):
    """Manager For users."""

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"


class Recipe(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time_minutes = models.IntegerField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name="recipes",
                             related_query_name="recipe")
    link = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "recipe"
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.title
