from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from client.forms.AddGoodsForm import AddGoodsForm
from client.forms.ChangeGoodsInfo import ChangeGoodsForm
from client.forms.DeleteGoodsForm import DeleteGoodsForm
from client.forms.LoginForm import LoginForm
from client.forms.PurchaseGoodsForm import PurchaseGoodsForm
from client.forms.SellGoodsForm import SellGoodsForm
from common.Password import verifyPassword
from rModels.Goods import *


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

@csrf_exempt
def addGoods(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	addGoodsForm = AddGoodsForm(request.POST)
	if not addGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单输入不合法'
		return JsonResponse(response)
	name = addGoodsForm.cleaned_data['name']
	amount = addGoodsForm.cleaned_data['amount']
	price = addGoodsForm.cleaned_data['price']
	purchasePrice = addGoodsForm.cleaned_data['purchasePrice']
	kind = addGoodsForm.cleaned_data['kind']

	result = r.table('goods').insert({
		'name' : name,
		'kind' : kind,
		'price' : price,
		'purchasePrice' : purchasePrice,
		'amount' : amount
	}).run()
	print(result)
	if result['inserted'] != 0:
		response['is_success'] = True
		response['message'] = '添加成功'
		return JsonResponse(response)
	response['is_success'] = False
	response['message'] = '添加失败'
	return JsonResponse(response)

@csrf_exempt
def deleteGoods(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	deleteGoodsForm = DeleteGoodsForm(request.POST)
	if not deleteGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单输入不合法'
		return JsonResponse(response)
	goodsID = deleteGoodsForm.cleaned_data['goodsID']
	result = r.table('goods').get(goodsID).delete().run()

	if result['skipped'] != 0:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result['deleted'] != 0:
		response['is_success'] = True
		response['message'] = '删除成功'
		return JsonResponse(response)
	response['is_success'] = False
	response['message'] = '删除失败'
	return JsonResponse(response)

@csrf_exempt
def goodsList(request):
	response = {}
	cursor = r.db('warehouse').table('goods').run()
	goodsList = list(cursor)
	print(goodsList)
	response['is_success'] = True
	response['goodsList'] = goodsList
	return JsonResponse(response)

@csrf_exempt
def changeGoodsInfo(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	changeGoodsForm = ChangeGoodsForm(request.POST)
	if not changeGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单输入不合法'
		return JsonResponse(response)
	goodsID = changeGoodsForm.cleaned_data['goodsID']
	name = changeGoodsForm.cleaned_data['name']
	amount = changeGoodsForm.cleaned_data['amount']
	price = changeGoodsForm.cleaned_data['price']
	purchasePrice = changeGoodsForm.cleaned_data['purchasePrice']
	kind = changeGoodsForm.cleaned_data['kind']
	result = r.table('goods').get(goodsID).update({
		"name" : name,
		"amount" : amount,
		"price" : price,
		"purchasePrice" : purchasePrice,
		"kind" : kind
	}).run()

	if result['skipped'] != 0:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result['unchanged'] != 0:
		response['is_success'] = False
		response['message'] = '未更改商品信息'
		return JsonResponse(response)

	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '更新商品信息失败'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '更新成功'
	return JsonResponse(response)

@csrf_exempt
def purchaseGoods(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	purchaseGoodsForm = PurchaseGoodsForm(request.POST)
	if not purchaseGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '变淡输入不合法'
		return JsonResponse(response)
	goodsID = purchaseGoodsForm.cleaned_data['goodsID']
	num = purchaseGoodsForm.cleaned_data['num']

	result, purchasePrice = r.table('goods').get(goodsID).do(
		lambda goodsObject:
		(
			r.branch(
				goodsObject,
				r.table('goods').get(goodsID).update({
					'amount': goodsObject['amount'] + num
				}),
				None
			),
			r.branch(
				goodsObject,
				goodsObject['purchasePrice'],
				None
			)
		)
	).run()

	if result == None:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result['skipped'] != 0:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '进货失败'
		return JsonResponse(response)
	purchasePriceSum = purchasePrice * num
	response['is_success'] = True
	response['message'] = '进货成功'
	response['purchasePriceSum'] = purchasePriceSum
	return JsonResponse(response)

@csrf_exempt
def sellGoods(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = True
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)

	sellGoodsForm = SellGoodsForm(request.POST)
	if not sellGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单输入不合法'
		return JsonResponse(response)
	goodsID = sellGoodsForm.cleaned_data['goodsID']
	num = sellGoodsForm.cleaned_data['num']

	result, price = r.table('goods').get(goodsID).do(
		lambda goodsObject:
		(
			r.branch(
				goodsObject,
				(
					r.branch(
						goodsObject['amount'] >= num,
						(
							r.table('goods').get(goodsID).update({
								'amount' : goodsObject['amount'] - num
							})
						),
						1
					)
				),
				None
			),
			r.branch(
				goodsObject,
				goodsObject['price'],
				None
			)
		)
	).run()

	if result == None:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result == 1:
		response['is_success'] = False
		response['message'] = '售出货物数量大于实际存储数量'
		return JsonResponse(response)

	if result['skipped'] != 0:
		response['is_success'] = False
		response['message'] = '货物不存在'
		return JsonResponse(response)

	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '售货失败'
		return JsonResponse(response)
	priceSum = price * num
	response['is_success'] = True
	response['message'] = '售货成功'
	response['priceSum'] = priceSum
	return JsonResponse(response)
