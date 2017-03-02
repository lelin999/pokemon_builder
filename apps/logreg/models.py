from __future__ import unicode_literals
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # Login checks and functions
    def login(self, **kwargs):
        print "** User manager activated **"
        print "** Checking login info **"
        status = {}
        messages = []
        username = kwargs['username'][0]
        password = kwargs['password'][0]
        if len(username) < 1 or len(password) < 1:
            messages.append("Login fields cannot be blank.")
        else:
            userinfo = User.objects.filter(username=username)
            if not userinfo:
                messages.append("Unable to find user. Please register.")
            elif not bcrypt.checkpw(password.encode(), userinfo[0].password.encode()):
                messages.append("Incorrect password.")
        if not messages:
            valid = True
            status.update({'user_id': userinfo[0].id})
        else:
            valid = False
            status.update({'messages': messages})
        status.update({'valid': valid})
        return status
    # Register checks and functions
    def register(self, **kwargs):
        print "** User manager activated **"
        print "** Checking registration form **"
        status = {}
        messages = []
        username = kwargs['username'][0]
        pword = kwargs['pword'][0]
        cpword = kwargs['c-pword'][0]
        if len(username) < 1:
            messages.append('Username is required.')
        elif len(username) < 2:
            messages.append('Username has to be at least 2 characters.')
        elif len(username) > 16:
            messages.append('Username cannot be more than 16 characters.')
        elif len(User.objects.filter(username__iexact=username)) > 0:
            messages.append('Username already taken.')
        if len(pword) < 1:
            messages.append('Password is required.')
        elif len(pword) < 8:
            messages.append('Password should be at least 8 characters.')
        elif pword != cpword:
            messages.append('Password fields do not match.')
        if not messages:
            valid = True
            messages.append('Thank you for registering! Please sign in.')
            pw_hash = bcrypt.hashpw(pword.encode(), bcrypt.gensalt())
            User.objects.create(username=username, password = pw_hash)
        else:
            valid = False
        status.update({'valid': valid, 'messages': messages})
        return status

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    rank = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    hp = models.IntegerField()
    atk = models.IntegerField()
    defense = models.IntegerField()
    spatk = models.IntegerField()
    spdef = models.IntegerField()
    speed = models.IntegerField()
    nature = models.CharField(max_length=255)
    typeI = models.CharField(max_length=255)
    typeII = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Roster(models.Model):
    pkmn = models.ManyToManyField(Pokemon, related_name="rosters")
    user = models.ForeignKey(User, related_name="belt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
