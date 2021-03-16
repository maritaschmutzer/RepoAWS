from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] == postData["password_confirm"]:
            pass
        else:
            errors["password_confirm"] = "Las contraseñas deben coincidir"
        if postData["fecha_cumpleanos"] > str(datetime.date.today()):
            errors["fecha_cumpleanos"] = "Fecha cumpleaños cannot be in the future!"
        todos_los_usuarios = User.objects.all() 
        for user in todos_los_usuarios:
            if postData['email'] != user.email:
                pass
            else:
                errors["email"] = "Email ya existe"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="")
    email= models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    fecha_cumpleanos = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Message(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
