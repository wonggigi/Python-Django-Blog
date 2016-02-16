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

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

import random
import json



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
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件',max_length=100)

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

def login(request):
    if request.method == 'POST':
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            blog_list = BlogsPost.objects.all()
            for blog in blog_list:
                blog.url = "/article/" + blog.title

            if user:
                request.session['username'] = username
                comments=Comment.objects.filter(title=blog_list[0].title)
                #return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
                return HttpResponseRedirect('/')
            else:
                print("Sad")
                return HttpResponseRedirect('/login/')
    else:
        uf = UserFormLogin()
        return render_to_response('login.html', {'uf': uf})

# Create your views here.
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))



def sendEmail(to_addr,request):
    from_addr = 'neuwangzhenzhong@163.com'#raw_input('From: ')
    password = 'wzz908868432'#raw_input('Password: ')
# 输入SMTP服务器地址:
    smtp_server = 'smtp.163.com'#raw_input('SMTP server: ')
# 输入收件人地址:
    #to_addr ='1045717286@qq.com' #raw_input('To: ')

    code=random.randint(100000, 999999)
    request.session['code'] = str(code)
    msg = MIMEText('验证码：'+str(code), 'plain', 'utf-8')
    msg['From'] = _format_addr(u' <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'来自鸡鸡哒的问候……', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

   

def register(request):
   
    if request.method == "POST" :
        if ('password' in request.POST.keys()):
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']  
            testIdCode=request.POST['test']
            if testIdCode==request.session['code'] :
                user = User()
                user.username = username
                user.password = password
                user.email = email
                
                user.userimg='/static/img/jslogo.png'
                user.save()
                blog_list = BlogsPost.objects.all()
                request.session['username'] = username
                print(username)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                for blog in blog_list:
                    blog.url = "/article/" + blog.title
                comments=Comment.objects.filter(title=blog_list[0].title)
                return HttpResponseRedirect('/')
                #return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else: 
                return render_to_response('register.html')
        else:
            print("1")
            req = json.loads((request.body).decode())
            if  not req["testEmail"]:
                print("2")
                response_data = {}  
                if req["username"]:
                    if User.objects.filter(username=req["username"]):
                        response_data['message'] = '该用户名已存在'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                    else:
                        response_data['message'] = '您可以使用这个用户名'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                elif req["email"]:
                    if User.objects.filter(email=req["email"]): 
                        response_data['message'] = '该邮箱已存在'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")  
                    elif req["requireIdcode"]:
                       response_data['message'] = '等待发送验证码'
                       sendEmail(req["email"],request)
                       return HttpResponse(json.dumps(response_data), content_type="application/json")
                    else:
                        response_data['message'] = '您可以使用这个邮箱'
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                
    else:
        return render_to_response('register.html')


def home(request, articleType,url='/'):
        request.session.set_expiry(0)
        username = request.session.get('username', False)
        print(username)
        if not username:
            pass#username = 'Tourist please login'
        if request.method == "POST":
            comment=Comment()
            comment.username=request.session.get('username', False)
            if url == '/':
                blog_list = BlogsPost.objects.filter(artcileType=articleType)
                thisBlog = BlogsPost.objects.get(title=blog_list[0].title)
                comment.title=thisBlog.title
                comment.time=datetime.datetime.now() 
            else:
                thisBlog = BlogsPost.objects.get(title=url)
                comment.title=thisBlog.title
                comment.time=datetime.datetime.now()
            comment.userimg='/static/img/jslogo.jpg'
            comment.body=request.POST.get('content',False)
            comment.save()
            if url=='/':
                comments=Comment.objects.filter(title=blog_list[0].title)
                return HttpResponseRedirect('/', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else:
                blog_list = BlogsPost.objects.filter(artcileType=articleType)
                thisBlog = BlogsPost.objects.get(title=url)
                comments=Comment.objects.filter(title=thisBlog.title)
                return HttpResponseRedirect(url, {'post': thisBlog, 'posts': blog_list, 'username': username,'comments':comments})
        else:
            blog_list = BlogsPost.objects.filter(artcileType=articleType)
            for blog in blog_list:
                blog.url = "/article/" +blog.artcileType + '/'+blog.title
            if url == '/':
                comments=Comment.objects.filter(title=blog_list[0].title)
                #print(blog_list[0].body)
                return render_to_response('home.html', {'posts': blog_list, 'post': blog_list[0], 'username': username,'comments':comments})
            else:
                thisBlog = BlogsPost.objects.get(title=url)
                comments=Comment.objects.filter(title=thisBlog.title)
                return render_to_response('home.html', {'post': thisBlog, 'posts': blog_list, 'username': username,'comments':comments})


def signOut(request):
    request.session['username']=False
    return HttpResponseRedirect('/')

def setting(request):
    print(request.session['username'])
    return render_to_response('usersetting.html',{'username':request.session['username']})
    
def index(request):
    username = request.session.get('username', False)
    comments=Comment.objects.filter(title='index')
    blog_list = BlogsPost.objects.all()
    for blog in blog_list: 
        blog.url = "/article/" +blog.artcileType+'/'+ blog.title
    return render_to_response('index.html', {'username': username,'comments':comments,'posts':blog_list})