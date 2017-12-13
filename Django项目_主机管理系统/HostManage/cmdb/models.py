from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    h = models.ManyToManyField("Host")
    g = models.ManyToManyField('Host_Group')

class Host(models.Model):
    hid = models.AutoField(primary_key=True)
    host_name = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    port = models.IntegerField()
    hostgroup = models.ForeignKey('Host_Group',null=True)

class Host_Group(models.Model):
    gid = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=64)