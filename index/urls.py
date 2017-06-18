from django.conf.urls import url

from index.views import *

urlpatterns = {
	url(r'^dbInit/$', dbInit),
	url(r'^doLogin/$', doLogin),
	url(r'^goodsList/$', goodsList),
	url(r'^addGoodsToCast/$', addGoodsToCart),
	url(r'^shoppingCast/$', shoppingCast),
	url(r'^payMoney/$', payMoney),
	url(r'^register/$', register),
	url(r'^cancelShopping', cancelShopping),
}