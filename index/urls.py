from django.conf.urls import url

from index.views import *

urlpatterns = {
	url(r'^dbInit/$', dbInit),
	url(r'^doLogin/$', doLogin),
	url(r'^goodsList/$', goodsList),
}