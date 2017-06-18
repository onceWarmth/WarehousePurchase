from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.Auth import *
from index.forms.DoLoginForm import DoLoginForm
from index.forms.PurchaseGoodsForm import PurchaseGoodsForm
from libs.rModels.User import *
from libs.rModels.Goods import *
from libs.rModels.Record import *
from libs.rModels.Info import *
import time


def dbInit(request):
	userInit()
	goodsInit()
	recordInit()
	infoInit()
	return HttpResponse("数据库初始化完成")

@csrf_exempt
def doLogin(request):
	print(request.encoding)
	print(request.POST)
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
	print(response)
	return JsonResponse(response)

@csrf_exempt
def register(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	print(request.POST)
	try:
		username = request.POST['username']
		password = request.POST['password']
	except:
		response['is_success'] = False
		response['message'] = '表单信息有误'
		return JsonResponse(response)
	userObject = r.table('users').get(username).run()
	if userObject:
		response['is_success'] = False
		response['message'] = '该用户已存在'
		return JsonResponse(response)
	salt = createSalt()
	method = "sha256"
	passwordHash = encryption(password, method, salt)
	result = r.table('users').insert({
		'id' : username,
		'password' : {
			'algorithm' : method,
			'hash' : passwordHash,
			'salt' : salt
		},
		'shoppingCast' : [],
		'type' : 'user'
	}).run()

	if result['inserted'] == 0:
		response['is_success'] = False
		response['message'] = '注册成功'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '注册成功'
	return JsonResponse(response)

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
def addGoodsToCart(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	purchaseGoodsForm = PurchaseGoodsForm(request.POST)
	if not purchaseGoodsForm.is_valid():
		response['is_success'] = False
		response['message'] = '表单输入信息不合法'
		return JsonResponse(response)
	goodsID = purchaseGoodsForm.cleaned_data['goodsID']
	num = purchaseGoodsForm.cleaned_data['num']
	if num <= 0:
		response['is_success'] = False
		response['message'] = '你在逗我吗？'
		return JsonResponse(response)
	goodsIDObject = r.table('goods').get(goodsID).run()
	if not goodsIDObject:
		response['is_success'] = False
		response['message'] = '商品不存在'
		return JsonResponse(response)
	count = r.table('goods').get(goodsID)['amount'].run()
	if count < num:
		response['is_success'] = False
		response['message'] = '您购买的商品数量大于存货数量'
		return JsonResponse(response)
	# user
	username = purchaseGoodsForm.cleaned_data['username']
	userObject = r.table('users').get(username).run()
	if not userObject:
		response['is_success'] = False
		response['message'] = '用户不存在'
		return JsonResponse(response)
	shoppingCast = userObject['shoppingCast']
	shoppingInfo = {}
	shoppingInfo['goodsID'] = goodsID
	shoppingInfo['num'] = num

	isExist = False
	for index in range(0, len(shoppingCast)):
		shopping = shoppingCast[index]
		if shopping['goodsID'] == shoppingInfo['goodsID']:
			shopping['num'] = shopping['num'] + shoppingInfo['num']
			isExist = True
			break
	if not isExist:
		shoppingCast.append(shoppingInfo)
	result_user = r.table('users').get(username).update({
		'shoppingCast': shoppingCast
	}).run()

	result = r.table('goods').get(goodsID).update({
		'amount': (count-num)
	}).run()

	if result['replaced'] == 0 or result_user['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '购买失败'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '购买成功'
	return JsonResponse(response)

@csrf_exempt
def shoppingCast(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	username = request.POST['username']

	userObject = r.db('warehouse').table('users').get(username).run()
	shoppingList = list(userObject['shoppingCast'])
	print(shoppingList)
	count = len(shoppingList)
	response['goodsList'] = ''
	for shopping in shoppingList:
		goods = {}
		goodsID = shopping['goodsID']
		goodsObject = r.table('goods').get(goodsID).run()
		goods['id'] = goodsObject['id']
		goods['name'] = goodsObject['name']
		goods['kind'] = goodsObject['kind']
		goods['price'] = str(goodsObject['price'])
		goods['purchasePrice'] = str(goodsObject['purchasePrice'])
		goods['amount'] = str(shopping['num'])
		response['goodsList'] = response['goodsList'] + goods['id'] + '$' + goods['name'] + '$' + \
														goods['amount'] + '$' + \
														goods['price'] + '$' + goods['purchasePrice'] + '$' + goods['kind']
		response['goodsList'] = response['goodsList'] + '&'
	response['count'] = str(count)
	return JsonResponse(response)

@csrf_exempt
def cancelShopping(request):
	response = {}
	num = 0
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)

	try:
		username = request.POST['username']
		goodsID = request.POST['goodsID']
	except:
		response['is_success'] = False
		response['message'] = '传入信息有误'
		return JsonResponse(response)
	userObject = r.table('users').get(username).run()
	if not userObject:
		response['is_success'] = False
		response['message'] = '用户不存在'
		return JsonResponse(response)
	shoppingCast = userObject['shoppingCast']
	for index in range(0, len(shoppingCast)):
		shopping = shoppingCast[index]
		if shopping['goodsID'] == goodsID:
			num = shopping['num']
			del shoppingCast[index]
			break
	result = r.table('users').get(username).update({
		'shoppingCast' : shoppingCast
	}).run()
	print(result)
	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '删除失败'
		return JsonResponse(response)
	goodsObject = r.table('goods').get(goodsID).run()
	if not goodsObject:
		response['is_success'] = False
		response['message'] = '商品不存在'
		return JsonResponse(response)
	goodsNum = goodsObject['amount']
	result = r.table('goods').get(goodsID).update({
		'amount' : goodsNum + num
	}).run()
	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '删除失败'
		return JsonResponse(response)
	response['is_success'] = True
	response['message'] = '移除成功'
	return JsonResponse(response)

@csrf_exempt
def payMoney(request):
	response = {}
	if request.method != 'POST':
		response['is_success'] = False
		response['message'] = '不是 POST 请求'
		return JsonResponse(response)
	try:
		username = request.POST['username']
	except:
		response['is_success'] = False
		response['message'] = '传入信息有误'
		return JsonResponse(response)
	userObject = r.table('users').get(username).run()
	if not userObject:
		response['is_success'] = False
		response['message'] = '该用户不存在'
		return JsonResponse(response)
	shoppingList = userObject['shoppingCast']
	if len(shoppingList) == 0:
		response['is_success'] = False
		response['message'] = '亲～你的购物车是空的呦～'
		return JsonResponse(response)
	result = r.table('users').get(username).update({
		'shoppingCast' : []
	}).run()
	if result['replaced'] == 0:
		response['is_success'] = False
		response['message'] = '付款失败'
		return JsonResponse(response)
	for shopping in shoppingList:
		num = shopping['num']
		goodsID = shopping['goodsID']
		goodsObject = r.table('goods').get(goodsID).run()
		price = goodsObject['price']
		priceSum = price * num
		r.table('records').insert({
			'time': time.time(),
			'num': str(num),
			'total': str(priceSum),
			'user': username,
			'isIncrease': True,
			'action': '买货',
			'goodsName': goodsObject['name'],
		}).run()
		total = r.table('infos').get('total')['total'].run()
		total = total + priceSum
		r.table('infos').get('total').update({
			'total': total
		}).run()
	response['is_success'] = True
	response['message'] = '付款成功'
	return JsonResponse(response)
