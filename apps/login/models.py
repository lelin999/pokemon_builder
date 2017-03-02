from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []     # array of error messages
        if len(postData["username"]) == 0:
            # if first name has not been entered
            errors.append("Please enter a username.")
        elif len(postData["username"]) < 2:
            errors.append("User name must be between 2-45 characters.")
        elif not re.search(r'^[A-Za-z]+$', postData["username"]):
            errors.append("User name must be letters only.")
        elif len(User.objects.filter(username=postData["username"])) > 0:
            # if list of users w/ this email is empty
            errors.append("Username is already registered.")
        if len(postData["password"]) < 8:
            errors.append("Password must be 8 or more characters.")
        if postData["confirm"] != postData["password"]:
            errors.append("Passwords do not match.")
        if len(errors) == 0:
            user = User.objects.create(username=postData["username"],pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return (True, user)
            # returns (success code, user object)
        else:
            return (False, errors)
            # returns (failure, error list)

    def authenticate(self, postData):
        if "username" in postData and "password" in postData:
            try:
                user = User.objects.get(username=postData["username"])
            except User.DoesNotExist:
                return (False, "Invalid username/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid username/password combination.")
        else:
            return (False, "Please enter login info.")


class User(models.Model):
    username = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
