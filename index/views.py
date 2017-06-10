from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.Auth import Auth, verifyPassword
from index.forms.DoLoginForm import DoLoginForm
from libs.rModels.User import *
from libs.rModels.Goods import *


def dbInit(request):
	userInit()
	goodsInit()
	return HttpResponse("数据库初始化完成")

@csrf_exempt
def doLogin(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '请求不是POST请求'
		return JsonResponse(response)
	doLoginForm = DoLoginForm(request.POST)
	if not doLoginForm.is_valid():
		response['is_success'] = False
		response['message'] = '字段传入信息有误'
		return JsonResponse(response)
	username = doLoginForm.cleaned_data["username"]
	password = doLoginForm.cleaned_data["password"]
	res = verifyPassword(password, username)
	if not res:
		response['is_success'] = False
		response['message'] = '用户名和密码错误'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '登录成功'
	return JsonResponse(response)

def goodsList(request):
	response = {}
	cursor = r.db('warehouse').table('goods').run()
	goodsList = list(cursor)
	print(goodsList)
	response['is_success'] = True
	response['goodsList'] = goodsList
	return JsonResponse(response)