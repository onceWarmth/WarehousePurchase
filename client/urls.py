from django.conf.urls import include, url
from client.views import *

urlpatterns = {
	url(r'^doLogin/$', doLogin),
}