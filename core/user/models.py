from typing import Any
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

# Create your models here.
class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id):

        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        
    def create_user(self, username, email, password=None, **kwargs):
        """ Crear y retornar un User con email, numero de teléfono y contraseña """
        if username is None:
            raise TypeError('El usuario debe tener un nombre de usuario obligatorio.')
        if email is None:
            raise TypeError('El usuario debe tener un email obligatorio.')
        if password is None:
            raise TypeError('El usuario debe tener una contraseña obligatoria.')

        user = self.model(username=username, email=self.normalize_email(email),
                           **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        """ Crear y devolver un usuario con permisos root de administrador"""
        if password is None:
            raise TypeError('La contraseña es obligatoria para el superusuario')
        if email is None:
            raise TypeError('El email es obligatorio para el superusuario.')
        if username is None:
            raise TypeError('El nombre de usuario es obligatorio para el superusuario.')
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(db_index=True, unique=True, 
                                 default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"