# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm
from models import User, SessionToken
from django.contrib.auth.hashers import make_password, check_password


def signup(request):
    logger = check_validation(request)
    if logger:
        response = redirect('feed/')
        return response
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            print (form)
            if form.is_valid():
                username = form.cleaned_data['username']
                name = form.cleaned_data['name']
                age = form.cleaned_data['age']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                gender = form.cleaned_data['gender']
                # saving data to DB
                user = User(name=name, username=username, age=age, phone=phone, password=make_password(password), email=email,
                            gender=gender)
                user.save()
                return render(request, 'success.html')
            else:
                return render(request, 'index.html')

    return render(request, 'index.html')


def login(request):
    message = None
    form = LoginForm(request.POST)
    print (form)
    # logger = check_validation(request)
    # if logger:
    #     response = redirect('feed/')
    #     return response
    # else:
    if request.method == "POST":
        print ('hello1')
        form = LoginForm(request.POST)
        print (form)
        if form.is_valid():
            print ('hello2')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()
            if user:
                print ('success')
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    message = 'Incorrect Password! Please try again!'
                    return render(request, 'login.html', {'response': message})
            else:
                message = 'Invalid User'
                return render(request, 'login.html', {'response': message})
        else:
            message = 'Fields cannot be kept blank'
            return render(request, 'login.html', {'response': message})

    elif request.method == 'GET':
        print ('hello3')
        return render(request, 'login.html', {'form': form})


def feed_view(request):
    return render(request, 'feed.html')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
# Create your views here.
