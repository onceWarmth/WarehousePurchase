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
	name = model_registry.get("User")
	if name:
		used = True
except KeyError:
	used = False

if (not used):
	class User(Model):
		pass
		"""
			声明一个remodel类
		"""


	class UserObjectHandler(ObjectHandler):
		pass

	def uid():
		nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
		randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
		if randomNum <= 10:
			randomNum = str(0) + str(randomNum)
		uniqueNum = str(nowTime) + str(randomNum)
		return uniqueNum


	class DefaultUser():
		"""docstring for DefauleUser"""

		# TODO 根据季总的业务逻辑设置初始化变量
		def __init__(self):
			self._user = {
				"id": uid(),
				"password": {
					"algorithm": "sha256",
					"hash":
						[12, 183, 41, 178, 6, 190, 185, 207, 56, 196,
						212, 183, 214, 181, 41, 12, 60, 62, 231, 25,
						226, 143, 104, 177, 119, 33, 157, 38, 43,
						164, 67, 81],
					 "salt": [55, 120, 86, 102, 53, 99]
				},
				"type": "user",
				"shoppingCast": []
				}

		# TODO  封装其他方法


	def userInit(**kargs):
		"""
			初始化数据库
			在安装的时候使用
		"""

		user = {
				"id": "user",
				"password": {
					"algorithm": "sha256",
					"hash":
						[12, 183, 41, 178, 6, 190, 185, 207, 56, 196,
						212, 183, 214, 181, 41, 12, 60, 62, 231, 25,
						226, 143, 104, 177, 119, 33, 157, 38, 43,
						164, 67, 81],
					 "salt": [55, 120, 86, 102, 53, 99]
				},
				"type": "user",
				"shoppingCast": [],
			}
		admin = {
				"id": "admin",
				"password": {
					"algorithm": "sha256",
					"hash":
						[12, 183, 41, 178, 6, 190, 185, 207, 56, 196,
						212, 183, 214, 181, 41, 12, 60, 62, 231, 25,
						226, 143, 104, 177, 119, 33, 157, 38, 43,
						164, 67, 81],
					 "salt": [55, 120, 86, 102, 53, 99]
				},
				"type": "admin",
				"shoppingCast": [],
			}
		salesperson = {
				"id": "salesperson",
				"password": {
					"algorithm": "sha256",
					"hash":
						[12, 183, 41, 178, 6, 190, 185, 207, 56, 196,
						212, 183, 214, 181, 41, 12, 60, 62, 231, 25,
						226, 143, 104, 177, 119, 33, 157, 38, 43,
						164, 67, 81],
					 "salt": [55, 120, 86, 102, 53, 99]
				},
				"type": "saleperson",
				"shoppingCast": [],
				}
		remodel.utils.create_tables()
		User(**user).save()
		# User(**user).save()
		User(**admin).save()
		User(**salesperson).save()
		return True

	dbName = "warehouse"

	remodel.connection.pool.configure(db=dbName)  # 默认数据库名为vpn

	conn = remodel.connection.pool.get()  # 获得rethinkdb连接实例,用于直接执行rethinkdb的查询操作

	used = True
# User(name="liuqi").save()
# user = User.get(name="liuqi")
# user["bandwidth"]["downstream"] = None
# user.save()
# username = request.session["user"]["username"]
# user = User.get(name=username)
