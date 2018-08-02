from __future__ import unicode_literals
import bcrypt
from django.db import models

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['username']) < 3 and (postData['username'].isalpha() != True):
            errors['username'] = 'Username must be at least 2 characters and only letters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'
        return errors

    
    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(username = postData['username'])) < 1:
            errors['wrong_username'] = 'Incorrect username or password' 
        else:
            u = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), u.password.encode()) != True:
                errors['wrong_password'] = 'Incorrect username or password'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    play = models.BooleanField()
    rating = models.IntegerField()
    win = models.IntegerField()
    loss = models.IntegerField()
    stack = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

    def __repr__(self):
        return "[{} {}]".format(self.id, self.first_name)

    def __str__(self):
        return "[{} {}]".format(self.id, self.first_name)


class TextManager(models.Manager):
    def text_validator(self, postData):
        errors = {}
        if len(postData['mess_content']) < 1:
            errors['username'] = 'Message cannot be blank'
        return errors

class Message(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name = 'message')
    profile = models.ForeignKey(User, related_name = 'mess_pro')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TextManager()

    def __str__(self):
        return "[{} {}]".format(self.user, self.profile)

    def __repr__(self):
        return "[{} {}]".format(self.user, self.profile)

class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = 'comment')
    message = models.ForeignKey(Message, related_name = 'comment')
    created_at = models.DateTimeField(auto_now_add = True)
    objects = TextManager()


    
