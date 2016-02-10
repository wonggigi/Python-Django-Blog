# coding:utf-8
from django.db import models
from django.shortcuts import render
from myapp.models import BlogsPost
from myapp.models import Comment
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from myapp.models import User
import datetime


def index(request):
    return HttpResponse(u"wd!!sf!")


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


class UserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=100)
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件：')


def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        print(uf)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(
                username__exact=username, password__exact=password)
            blog_list = BlogsPost.objects.all()
            for blog in blog_list:
                blog.url = "/article/" + blog.title

            if user:
                request.session['username'] = username
                comments=Comment.objects.filter(title=blog_list[0].title)
                return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html', {'uf': uf})

# Create your views here.


def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            # 将表单写入数据库
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            # 返回注册成功页面
            blog_list = BlogsPost.objects.all()
            request.session['username'] = username
            for blog in blog_list:
                blog.url = "/article/" + blog.title
            comments=Comment.objects.filter(title=blog_list[0].title)
            return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
    else:
        uf = UserForm()
        return render_to_response('register.html', {'uf': uf})


def home(request, url='/'):
        username = request.session.get('username', 'anybody')
        if not username:
            username = 'Tourist please login'
        if request.method == "POST":
            comment=Comment()
            comment.username=request.session.get('username', 'anybody')
            if url == '/':
                blog_list = BlogsPost.objects.all()
                thisBlog = BlogsPost.objects.get(title=blog_list[0].title)
                comment.title=thisBlog.title
                comment.time=datetime.datetime.now() 
            else:
                thisBlog = BlogsPost.objects.get(title=url)
                comment.title=thisBlog.title
                comment.time=datetime.datetime.now() 
            comment.body=request.POST['content']
            comment.save()
            if url=='/':
                comments=Comment.objects.filter(title=blog_list[0].title)
                return HttpResponseRedirect('/', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else:
                blog_list = BlogsPost.objects.all()
                thisBlog = BlogsPost.objects.get(title=url)
                comments=Comment.objects.filter(title=thisBlog.title)
                return HttpResponseRedirect(url, {'post': thisBlog, 'posts': blog_list, 'username': username,'comments':comments})
        else:
            blog_list = BlogsPost.objects.all()
            for blog in blog_list:
                blog.url = "/article/" + blog.title
            if url == '/':
                comments=Comment.objects.filter(title=blog_list[0].title)
                print(comments[0].body+","+comments[1].body)
                return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else:
                thisBlog = BlogsPost.objects.get(title=url)
                comments=Comment.objects.filter(title=thisBlog.title)
                return render_to_response('home.html', {'post': thisBlog, 'posts': blog_list, 'username': username,'comments':comments})
