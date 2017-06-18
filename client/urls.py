from django.conf.urls import include, url
from client.views import *

urlpatterns = {
	url(r'^doLogin/$', doLogin),
	url(r'^addGoods/$', addGoods),
	url(r'^deleteGoods/$', deleteGoods),
	url(r'^goodsList/$', goodsList),
	url(r'^changeGoodsInfo/$', changeGoodsInfo),
	url(r'^purchaseGoods/$', purchaseGoods),
	url(r'^sellGoods/$', sellGoods),
	url(r'^records/$', records),
}