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
from common.Password import *
from rModels.Goods import *
from rModels.Record import *
from rModels.Info import *
import time


@csrf_exempt
def doLogin(request):
	print(request.POST)
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是POST请求'
		return JsonResponse(response)
	# loginForm = LoginForm(request.POST)
	# if not loginForm.is_valid():
	# 	response['is_success'] = False
	# 	response['message'] = '表单不合法'
	# 	return JsonResponse(response)
	username = request.POST['username']
	password = request.POST['password']
	print(username)
	# username = loginForm.cleaned_data['username']
	# password = loginForm.cleaned_data['password']
	res = verifyPassword(password, username)
	if not res:
		response['is_success'] = False
		response['message'] = '用户名或密码错误'
		return JsonResponse(response)
	user = r.table('users').get(username).run()
	userType = user['type']
	if userType == 'user':
		response['is_success'] = False
		response['message'] = '你没有权限访问该系统'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '用户名和密码正确'
	return JsonResponse(response)

@csrf_exempt
def addGoods(request):
	print(request.encoding)
	print(request.POST)
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
	count = r.table('goods').count().run()
	goodsID = ""
	if count < 10:
		goodsID = "000" + str(count + 1)
	elif count < 100:
		goodsID = "00" + str(count + 1)
	elif count < 1000:
		goodsID = "0" + str(count + 1)
	else:
		goodsID = str(count + 1)
	result = r.table('goods').insert({
		'id' : goodsID,
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
	count = r.table('goods').count().run()
	response['goodsList'] = ''
	for goods in goodsList:
		goods['price'] = str(goods['price'])
		goods['purchasePrice'] = str(goods['purchasePrice'])
		goods['amount'] = str(goods['amount'])
		response['goodsList'] = response['goodsList'] + goods['id'] + '$' + goods['name'] + '$' + \
														goods['amount'] + '$' + \
														goods['price'] + '$' + goods['purchasePrice'] + '$' + goods['kind']
		response['goodsList'] = response['goodsList'] + '&'
	response['count'] = str(count)
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
	goodsObject = r.table('goods').get(goodsID).run()
	r.table('records').insert({
		'time': time.time(),
		'num': str(num),
		'total': str(purchasePriceSum),
		'user': "admin",
		'isIncrease': False,
		'action': '进货',
		'goodsName': goodsObject['name'],
	}).run()
	total = r.table('infos').get('total')['total'].run()
	total = total - purchasePriceSum
	r.table('infos').get('total').update({
		'total': total
	}).run()
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
	goodsObject = r.table('goods').get(goodsID).run()
	r.table('records').insert({
		'time' : time.time(),
		'num' : str(num),
		'total' : str(priceSum),
		'user' : "salesperson",
		'isIncrease' : True,
		'action' : '售货',
		'goodsName' : goodsObject['name'],
	}).run()
	total = r.table('infos').get('total')['total'].run()
	total = total + priceSum
	r.table('infos').get('total').update({
		'total' : total
	}).run()
	response['is_success'] = True
	response['message'] = '售货成功'
	response['priceSum'] = priceSum
	return JsonResponse(response)

@csrf_exempt
def records(request):
	response = {}
	cursor = r.db('warehouse').table('records').order_by('time').run()
	recordsObjects = list(cursor)
	recordsList = []
	for record in recordsObjects:
		recordsList.insert(0, record)
	count = len(recordsList)
	print(count)
	response['records'] = ''
	for record in recordsList:
		action = record['action']
		goodsName = record['goodsName']
		isIncrease = str(record['isIncrease'])
		num = str(record['num'])
		time = timestampToString(record['time'])
		total = str(record['total'])
		user = str(record['user'])
		response['records'] = response['records'] + time + '$' + user + '$' + action + '$'\
													+ goodsName + '$' + num + '$' + total + '$' + isIncrease
		response['records'] = response['records'] + '&'
	response['count'] = str(count)
	amount = r.table('infos').get('total')['total'].run()
	response['total'] = str(amount)
	return JsonResponse(response)

def timestampToString(jsTimestamp):
	if jsTimestamp == None:
		return "没有时间"
	timestamp = jsTimestamp + 8 * 60 * 60
	timeArray = time.localtime(timestamp)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyleTime
