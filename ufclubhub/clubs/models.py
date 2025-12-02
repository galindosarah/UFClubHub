from asyncio import Event

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import ForeignKey
from django.db.models import CompositePrimaryKey
from django.conf import settings


class Permissions(models.Model):
    permission_level = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.permission_level}: {self.description}"

    class Meta:
        managed = False
        db_table = 'permissions'


#Reflects Users relation in db
class  Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    ufid = models.CharField(unique=True, max_length=10, primary_key=True)
    permissions = models.ForeignKey(
        Permissions,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True,
        default=2,
        db_column='permissions'  # explicitly match your DB column
    )

    #any null permissions will be treated the same as user level

    class Meta:
        managed = False
        db_table = 'users'

    #add user to db // forms.py will do input validation before calling this
    @classmethod
    def add_user(cls, name, email, ufid, permissions=None):
        if permissions is None:
            try:
                permissions = Permissions.objects.get(permission_level=2)
            except ObjectDoesNotExist:
                permissions = None
        user = cls.objects.create(name=name, email=email, ufid=ufid, permissions=permissions)
        return user

    #selects user whose ufid=self.ufid and deletes the row
    @classmethod
    def delete_user(cls, ufid):
        return cls.objects.filter(ufid=ufid).delete()

    #selects for ufid and updates permissions for club admin
    @classmethod
    def update_user_permissions(cls, ufid, new_permissions):
        return cls.objects.filter(ufid=ufid).update(permissions=new_permissions)

    def __str__(self):
        return self.name

class Login(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name='login_record',
        primary_key=True,
        db_column='ufid'
    )
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'login'



class Club(models.Model):
    club_name = models.CharField(max_length=100, primary_key=True) # stores the club name
    permissions = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE,
        db_column='exec_permission_level')
    category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'club'

    #input validation somewhere else // forms.py
    @classmethod
    def add_club(cls, club_name, category, permissions=None):
        return cls.objects.create(club_name=club_name, category=category, permissions=permissions)

    @classmethod
    def remove_club(cls, club_name):
        return cls.objects.filter(club_name=club_name).first()

    @classmethod
    def retrieve_club(cls, name):
        return cls.objects.filter(club_name=name)

    @classmethod
    def retrieve_all_clubs(cls):
        return cls.objects.all()

    @classmethod
    def search_by_name(cls, query):
        #reusable search
        if not query:
            return cls.retrieve_all_clubs()
        return cls.objects.filter(name__icontains=query)

    def __str__(self):
        return self.club_name


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='membership', db_column='ufid')
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members', db_column='club_name')
    date_joined = models.DateField()
    permissions_level = models.IntegerField()

    class Meta:
        unique_together = (('user', 'club_name'),)
        managed = False
        db_table = 'members'

    #these need to be updated to not instantiate everytime(class method, etc.)
    @classmethod
    def add_member(cls, user, club_name, date_joined, permissions_level):
        return cls.objects.create(user=user, club_name=club_name, date_joined=date_joined, permissions_level=permissions_level)

    @classmethod
    def remove_member_one_club(cls, user, club_name):
        return cls.objects.filter(user=user, club_name=club_name).delete()

    @classmethod
    def remove_member_all_clubs(cls, user):
        return cls.objects.filter(user=user).delete()

    @classmethod
    def retrieve_user_clubs(cls, user):
        memberships = cls.objects.filter(user=user).select_related('club_name')
        return [m.club_name for m in memberships]

    def __str__(self):
        return f"{self.user.name} in {self.club_name.name}"

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_datetime = models.DateTimeField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events', db_column='club_name')

    class Meta:
        managed = False
        db_table = 'events'

    @classmethod
    def add_event(cls, title, description, event_datetime, club):
        return cls.objects.create(
            title=title,
            description=description,
            event_datetime=event_datetime,
            club=club
        )

    ##retrieve events for a specific club
    @classmethod
    def retrieve_event(cls, club):
        return cls.objects.filter(club=club)

    @classmethod
    def retrieve_events_for_clubs(cls, clubs):
        return cls.objects.filter(club__in=clubs).order_by('event_datetime')

    def __str__(self):
        return f"{self.title} ({self.club.name})"


class Announcements(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_at = models.TimeField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements', db_column='club_name')

    class Meta:
        managed = False
        db_table = 'announcements'

    @classmethod
    def add_announcement(cls, title, content, posted_at, club):
        return cls.objects.create(
            title=title,
            content=content,
            posted_at=posted_at,
            club=club
        )

    #all announcements for one club, do i need all? how can i filter for just what i want?
    @classmethod
    def retrieve_announcement(cls, club):
        return cls.objects.filter(club=club)

    def __str__(self):
        return f"{self.title} ({self.club.name})"

class ClubLogin(models.Model):
    club = models.OneToOneField(
        Club,
        on_delete=models.CASCADE,
        related_name='login_record',
        primary_key=True,
        to_field='club_name',
        db_column='club'
    )
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    permission = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE,
        db_column='permission'
    )

    class Meta:
        managed = False
        db_table = 'ClubLogin'

    def __str__(self):
        return f"{self.username} for {self.club.club_name}"



