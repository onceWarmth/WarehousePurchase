import random
import hashlib
from libs.rModels.User import *

def createSalt():
  salt = []
  for i in range(0, 6):
    salt.append(random.randint(0, 255))
  return salt


def encryption(password, metnod, salt):
  password_UTF8 = password.encode('utf-8')
  password2 = bytes(salt) + password_UTF8
  encodeMode = hashlib.sha256()
  if metnod == 'md5':
    encodeMode = hashlib.md5()
  encodeMode.update(password2)
  temp = encodeMode.digest()
  result = []
  for i in temp:
    result.append(i)

  return result

def verifyPassword(password, username):
  user = User.get(id=username)
  if user:
    salt = user["password"]["salt"]
    algorithm = user["password"]["algorithm"]
    realPassword = user["password"]["hash"]
    password = encryption(password, algorithm, salt)
    if password == realPassword:
      return True
  return False
