from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

class Article( models.Model):
    id = models.IntegerField( primary_key = True )
    title = models.TextField(max_length= 200, blank = False, null = False)
    hackernews_url = models.URLField( blank =False, null = False)
    url = models.URLField('')
    posted_age = models.TextField(max_length=50, null = False, blank = False)
    here_posted_on = models.DateTimeField(default=timezone.now)
    upvotes = models.IntegerField(default=0, null = False)
    comments = models.IntegerField(default=0, null = False)
    def __str__(self):
        return self.title

class UserPreferences( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    article = models.ForeignKey( Article, on_delete = models.CASCADE )
    is_read = models.BooleanField( default = False)
    is_deleted = models.BooleanField( default = False )
    read_timestamp = models.DateTimeField(default= timezone.now)
    delete_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

def get_articles_for_user_orderby_posted_date( curr_user, max_articles = 90):
    is_deleted_prefereences = UserPreferences.objects.filter(
                            user=curr_user, is_deleted = True)
    avoid_article_ids = [ pref.article.id for pref in is_deleted_prefereences]
    is_read_prefereences = UserPreferences.objects.filter(
                            user=curr_user, is_read = True, is_deleted = False)
    read_article_ids = [ pref.article.id for pref in is_read_prefereences]
    news_articles = Article.objects.all().order_by('-here_posted_on')[:max_articles]
    news_articles = [ article for article in news_articles if article.id not in avoid_article_ids]
    result = {
        'news_articles':news_articles,
        'read_article_ids':read_article_ids,
    }
    return result

def get_deleted_articles_for_user_orderby_posted_date( curr_user):
    is_deleted_prefereences = UserPreferences.objects.filter(
                            user=curr_user, is_deleted = True)
    include_article_ids = [ pref.article.id for pref in is_deleted_prefereences]
    is_read_prefereences = UserPreferences.objects.filter(
                            user=curr_user, is_read = True, is_deleted = False)
    read_article_ids = [ pref.article.id for pref in is_read_prefereences]
    news_articles = list()
    for article_id in include_article_ids:
        article = Article.objects.get(id = article_id)
        news_articles.append( article)
    news_articles = sorted( news_articles, key = lambda x : (x.here_posted_on), reverse=True)
    result = {
        'news_articles':news_articles,
        'read_article_ids':read_article_ids,
    }
    return result
