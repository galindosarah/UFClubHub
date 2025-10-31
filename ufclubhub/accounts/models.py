from django.db import models

class  Account(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # grad_year = models.IntegerField()
    password = models.CharField(max_length=128)
    # clubs = models.ManyToManyField(Club, related_name = "member")
    # is_club = models.BooleanField(default=False)
    # admin_code = models.IntegerField(max_length = 50, blank = True)
    # is_admin = models.BooleanField(default=False)

# Create your models here.
