from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import Article

LOGIN_PAGE = 'registration/login.html'
SIGNUP_PAGE = 'registration/signup.html'
RESET_PASSWORD_PAGE = 'dashboard/reset_password.html'
SUCCESS_PAGE = 'dashboard/success.html'
WELCOME_PAGE = 'dashboard/home.html'

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

def reset_pass_view( request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['user_email']
            user_password = form.cleaned_data['user_password']
            return HttpResponseRedirect(SUCCESS_PAGE)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ResetPasswordForm()
    return render(request, SIGNUP_PAGE, {'form': form})

from .apps import DashboardConfig
@login_required(redirect_field_name='login')
def index_view( request ):
    # obj = DashboardConfig.news_fetcher_obj
    # obj.downloadData()
    # obj.saveToDb()
    news_articles = Article.objects.all().order_by('here_posted_on')[:90]
    has_data = len( news_articles) == 90
    context = {
        'news_articles':news_articles,
        'has_data':has_data,
    }
    return render(request, WELCOME_PAGE, context = context)
