from django.conf.urls import include, url
from login.views import *

urlpatterns = {
	url(r'^dbInit/$', dbInit),
	url(r'^doLogin/$', doLogin),
}