# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=30, unique='True')
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50,null=True)
    gender = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()


class PostModel(models.Model):
    user = models.ForeignKey(User)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


