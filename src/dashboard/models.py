from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Article( models.Model):
    id = models.IntegerField( primary_key = True )
    title = models.TextField(max_length= 200, blank = False, null = False)
    hackernews_url = models.URLField( blank =False, null = False)
    url = models.URLField()
    posted_age = models.TextField(max_length=50, null = False, blank = False)
    here_posted_on = models.DateTimeField()
    upvotes = models.IntegerField( null = False)
    comments = models.IntegerField( null = False)
    def __str__(self):
        return self.title
