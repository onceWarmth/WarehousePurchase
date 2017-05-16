from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from client.forms.LoginForm import LoginForm
from common.Password import verifyPassword

@csrf_exempt
def doLogin(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是POST请求'
		return JsonResponse(response)
	loginForm = LoginForm(request.POST)
	if not loginForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单不合法'
		return JsonResponse(response)
	username = loginForm.cleaned_data['username']
	password = loginForm.cleaned_data['password']
	res = verifyPassword(password, username)
	if not res:
		response['is_success'] = False
		response['message'] = '用户名或密码错误'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '用户名和密码正确'
	return JsonResponse(response)