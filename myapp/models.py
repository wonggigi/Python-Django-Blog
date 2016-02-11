from django.db import models
from django.contrib import admin
from tinymce import models as tinymce_models  

#from __future__  import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
#################

class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    body = tinymce_models.HTMLField()  
    timestamp = models.DateTimeField()


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp','body')


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')



class Comment(models.Model):
	title = models.CharField(max_length=150)
	username=models.CharField(max_length=50)
	time=models.DateTimeField()
	body=tinymce_models.HTMLField()  

class CommentAdmin(admin.ModelAdmin):
	list_display=('title','username','time','body')

admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BlogsPost, BlogPostAdmin)
