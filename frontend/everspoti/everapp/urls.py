from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]