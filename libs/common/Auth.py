# coding:utf-8
from libs.rModels.User import *
from libs.common.Password import *
import re

class Auth(object):
  """docstring for Auth"""
  def __init__(self,request):
    super(Auth, self).__init__()
    self.request = request
    self.permission = {

    }

  def verify(self,username,password,method="sha256"):
    #验证函数
    res = User.get(id = username)
    if res:
      salt = res["password"]["salt"]
      algorithm = res["password"]["algorithm"]
      hashPass = res["password"]["hash"]
      result = encryption(password, algorithm, salt)
      if result == hashPass:
        return res
    return False
  
  def login(self,username,password,method="sha256"):
    user = self.verify(username,password)
    if user:
      self.request.session["user"] = {
        "username":user["id"],
        "type":user["type"],
      }
      # set log
      return True
    else:
      return False

  def logout(self):
    try:
      username=  self.request.session["user"]["username"]
      del self.request.session['user']
      return username
    except KeyError:
      return False

  def auth(self):
    path = self.request.path
    userType = self.identity()
    # user = self.request.session["user"]["username"]
    if not userType:
      return False

    patterns = self.permission[userType]
    
    for pattern in patterns:
      if re.match(pattern,path) != None:
        return True
    return False
  
  def identity(self):
    try:
      userType = self.request.session["user"]["type"]
    except KeyError:
      userType = "visitor"
    if userType=="admin":
      userType = "adminUser"
    return userType
