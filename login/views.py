from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from common.Auth import Auth
from libs.rModels.User import userInit
from login.forms.DoLoginForm import DoLoginForm


def dbInit(request):
	userInit()
	return HttpResponse("数据库初始化完成")

@csrf_exempt
def doLogin(request):
	response = {}
	if request.method != 'POST':
		response['type'] = 'danger'
		response['message'] = '请求不是POST请求'
		return JsonResponse(response)
	doLoginForm = DoLoginForm(request.POST)
	if not doLoginForm.is_valid():
		response['type'] = 'danger'
		response['message'] = '字段传入信息有误'
		return JsonResponse(response)
	username = doLoginForm.cleaned_data["username"]
	password = doLoginForm.cleaned_data["password"]
	auth = Auth(request)
	res = auth.login(username, password)
	if not res:
		response['type'] = 'warning'
		response['message'] = '用户名和密码错误'
		return JsonResponse(response)
	response['type'] = 'success'
	response['message'] = '登录成功'
	return JsonResponse(response)



