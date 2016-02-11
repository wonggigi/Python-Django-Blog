from django.conf.urls import patterns, include, url
#from DjangoUeditor import urls as DjangoUeditor_urls
#import django_summernote
from django.contrib import admin
admin.autodiscover()
 
urlpatterns = patterns('',
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'myapp.views.home', name='home'),  # new
    url(r'^article/(\w+)', 'myapp.views.home', name='home'),
    url(r'^add/(\d+)/(\d+)/$', 'myapp.views.add2', name='add2'),
    url(r'^add/$', 'myapp.views.add', name='add'), # 注意修改了这一行
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$','myapp.views.register',name = 'register'),
    url(r'^login/$','myapp.views.login',name = 'login'),
    #url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/js'}),  
   # url(r'^tinymce/', include('tinymce.urls'))
    #url(r'^summernote/', include('django_summernote.urls')),
  #  url(r'^ueditor/', include('DjangoUeditor.urls' )),
)