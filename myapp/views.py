# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm
from models import User, SessionToken, PostModel
from django.contrib.auth.hashers import make_password, check_password
from imgurpython import ImgurClient


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
    # print (form)
    # # logger = check_validation(request)
    # # if logger:
    # #     response = redirect('feed/')
    # #     return response
    # # else:
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
                    response = redirect('/post/')
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


def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                path = str(post.image.url)
                client = ImgurClient('075ba389c237327', '87fb26c7f1af1203fe71c6b810662290462fa6bd')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                return redirect('/feed/')
        elif request.method == 'GET':
            form = PostForm()
            return render(request, 'post.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')




# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
# Create your views here.
