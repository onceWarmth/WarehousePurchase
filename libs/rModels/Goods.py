# coding:utf-8
import remodel.utils
import remodel.connection
import rethinkdb as r
# 用来产生uid
import datetime
import random

from remodel import models
from remodel.models import Model
from remodel.registry import model_registry
from remodel.object_handler import ObjectHandler, ObjectSet


# 通过判断model是否被注册判断文件是否被引用
used = False
try:
	name = model_registry.get("Goods")
	if name:
		used = True
except KeyError:
	used = False

if (not used):
	class Goods(Model):
		pass
		"""
			声明一个remodel类
		"""


	class GoodsObjectHandler(ObjectHandler):
		pass

	def uid():
		nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
		randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
		if randomNum <= 10:
			randomNum = str(0) + str(randomNum)
		uniqueNum = str(nowTime) + str(randomNum)
		return uniqueNum


	class DefaultGoods():
		"""docstring for DefauleGood"""

		# TODO 根据季总的业务逻辑设置初始化变量
		def __init__(self):
			self._goods = {
				"name": "Good1",
				"amount": 1,
				"price": 1.12,
				"purchasePrice": 1.00,
				"kind": "食品类",
			}

		# TODO  封装其他方法


	def goodsInit(**kargs):
		"""
			初始化数据库
			在安装的时候使用
		"""

		goods = {
			"name": "Good1",
			"amount": 1,
			"price": 1.12,
			"purchasePrice": 1.00,
			"kind": "食品类",
		}
		remodel.utils.create_tables()
		Goods(**goods).save()
		return True

	dbName = "warehouse"

	remodel.connection.pool.configure(db=dbName)  # 默认数据库名为vpn

	conn = remodel.connection.pool.get()  # 获得rethinkdb连接实例,用于直接执行rethinkdb的查询操作

	used = True
