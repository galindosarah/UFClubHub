from django.db import models
class Club(models.Model):
    name = models.CharField(max_length=100) # stores the club name
    bio = models.TextField() # stores the club description
    year = models.IntegerField() # stores the year the club was founded
    members = models.IntegerField(default=0) # stores the amount of members in the club

class  Account(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # grad_year = models.IntegerField()
    password = models.CharField(max_length=128)
    # clubs = models.ManyToManyField(Club, related_name = "member")
    # is_club = models.BooleanField(default=False)
    # admin_code = models.IntegerField(max_length = 50, blank = True)
    # is_admin = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True,blank = True)
    recipient = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Announcements(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField(null=True, blank=True)

