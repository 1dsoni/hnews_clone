from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Article, UserPreferences
from .models import get_articles_for_user_orderby_posted_date
from .models import get_deleted_articles_for_user_orderby_posted_date

LOGIN_PAGE = 'registration/login.html'
SIGNUP_PAGE = 'registration/signup.html'
WELCOME_PAGE = 'dashboard/home.html'
DELETED_ARTICLE_PAGE = 'dashboard/deleted_articles.html'

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    else:
        form = UserCreationForm()
    return render(request, SIGNUP_PAGE, {'form': form})

from .apps import DashboardConfig
@login_required(redirect_field_name='login')
def index_view( request ):
    result = get_articles_for_user_orderby_posted_date(request.user,max_articles=90)
    context = {
        'read_article_ids':result['read_article_ids'],
        'news_articles':result['news_articles'],
        'has_data':True,
    }
    return render(request, WELCOME_PAGE, context = context)

@login_required(redirect_field_name='login')
def deleted_articles_view( request ):
    result = get_deleted_articles_for_user_orderby_posted_date(request.user)
    context = {
        'read_article_ids':result['read_article_ids'],
        'news_articles':result['news_articles'],
        'has_data':True,
    }
    return render(request, DELETED_ARTICLE_PAGE, context = context)

@login_required(redirect_field_name='login')
def delete_article( request, article_id ):
    myuser = get_object_or_404(User, username= request.user.username)
    myarticle = get_object_or_404(Article, id=article_id)
    pref = UserPreferences.objects.filter(user = myuser, article = myarticle)
    if(len(pref)==0):
        pref = UserPreferences()
        pref.user = myuser
        pref.article = myarticle
        pref.is_deleted = True
        pref.save()
    else:
        pref[0].is_deleted = True
        pref[0].save()
    return redirect('home')

@login_required(redirect_field_name='login')
def undelete_article( request, article_id ):
    myuser = get_object_or_404(User, username= request.user.username)
    myarticle = get_object_or_404(Article, id=article_id)
    pref = UserPreferences.objects.filter(user = myuser, article = myarticle, is_deleted = True)
    if(len(pref)==0):
        pass
    else:
        pref[0].is_deleted = False
        pref[0].save()
    return redirect('deleted_articles')

@login_required(redirect_field_name='login')
def read_article( request, article_id):
    myuser = get_object_or_404(User, username= request.user.username)
    myarticle = get_object_or_404(Article, id=article_id)
    pref = UserPreferences.objects.filter(user = myuser, article = myarticle)
    if(len(pref)==0):
        pref = UserPreferences()
        pref.user = myuser
        pref.article = myarticle
        pref.is_read = True
        pref.save()
    else:
        pref[0].is_read = True
        pref[0].save()
    return redirect('home')
