import json
import random
import time

import redis

# 密钥常量配置
KEY_COUNT = 256
KEY_VALUE_CHAR = "abcdefghijklmnopqrstuvwxyz_1234567890ABCDEFJHIJKLMNOPQRSTUVWXYZ"

class Key():

  def __init__(self):
    self.r=redis.Redis(host='localhost', port=6379, db=0)

  def addKeyToDbAndGetKey917List(self, count, packageId, packageName, createAdmin):
    keyList = self.createKeyList(count)
    # self.r.flushall()
    Key917List = []
    for keyValue in keyList:
      keyObject = {}
      keyObject["key"] = keyValue
      keyObject["num"] = self.createCardNum()
      keyObject["packageId"] = packageId
      keyObject["packageName"] = packageName
      keyObject["createTime"] = int(time.time())*1000
      keyObject["createAdmin"] = createAdmin
      keyObject["isUsed"] = False
      keyObject["usedTime"] = None
      keyObject["user"] = None

      key_lenth = self.r.hlen("warehouse")
      self.r.hsetnx("warehouse", keyValue, json.dumps(keyObject))
      self.r.hsetnx("warehouseindex", key_lenth+1, keyValue)

      key917CardNum = keyObject["num"]
      key917Value = keyObject["key"]
      key917 = key917CardNum + " " + key917Value
      Key917List.append(key917)

    return Key917List



  def createKey(self):
    keyCharList = []
    for i in range(0, KEY_COUNT):
      keyChar = random.choice(KEY_VALUE_CHAR)
      keyCharList.append(keyChar)
    key = "".join(keyCharList)
    return key

  def createKeyList(self, count):
    keyList = []
    for i in range(0, count):
      while True:
        keyValue = self.createKey()
        keyObject = self.r.hexists("warehouse", keyValue)
        if not keyObject:
          break
      keyList.append(keyValue)
    return keyList

  def createCardNum(self):
    nowTime = int(time.time())
    ran = random.randint(0, 100)
    ran = str(ran)
    if int(ran) < 100:
      ran = str(0) + ran
    if int(ran) < 10:
      ran = str(0) + ran
    cardNum = str(nowTime) + ran
    return cardNum


  def getAdminManagerKeyList(self):
    keyList = []
    keys = self.r.hvals("warehouse")
    for keydetail in keys:
      key = json.loads(keydetail.decode())
      keyList.append(key)
    return keyList

  def getAdminManagerKeyList(self, low, high):
    keyList = []
    if high>self.r.hlen("warehouseindex"):
      high = self.r.hlen("warehouseindex")
    if low<1:
      low = 1
    n = low
    if low == high:
      high = high+1
    while n<high:
      key = self.r.hget("warehouseindex", n).decode()
      keyValue = {}
      if key:
        key_value = self.r.hget("warehouse", key).decode()
        keyValue = json.loads(key_value)
      keyList.append(keyValue)
      n = n+1
    return keyList

  def getKeysCount(self):
    count = self.r.hlen("warehouseindex")
    return count

  def get(self,key):
    keyObject = self.r.hexists("warehouse", key)
    if keyObject == 0:
      return False
    keyObject = json.loads(self.r.hget("warehouse", key).decode("utf-8"))
    return keyObject

  def use(self,key):
    keyObject = self.r.hexists("warehouse", key)
    if keyObject == 0:
      return False
    keyObject = json.loads(self.r.hget("warehouse", key).decode("utf-8"))
    keyObject["isUsed"] = True
    self.r.hset("warehouse", key, json.dumps(keyObject))
    return True