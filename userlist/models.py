from django.db import models


class UserList(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    own_code = models.CharField(max_length=50)
    refer_code = models.CharField(max_length=50)
    position = models.IntegerField(default=0)
