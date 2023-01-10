import os
import datetime


def create_folder(path):
   # 年
   year =datetime.datetime.now().strftime('%Y')
   # 年-月
   month = datetime.datetime.now().strftime('%Y-%m')
   # 年-月-日
   day = datetime.datetime.now().strftime('%Y-%m-%d')
   foldername = os.path.join(path, year, month, day)
   # 文件路径
   word_name = os.path.exists(foldername)
   # 判断文件是否存在：不存在创建
   if not word_name:
       os.makedirs(foldername)


def PathIsExit(path):
   # 年
   year =datetime.datetime.now().strftime('%Y')
   # 年-月
   month = datetime.datetime.now().strftime('%Y-%m')
   # 年-月-日
   day = datetime.datetime.now().strftime('%Y-%m-%d')
   foldername = os.path.join(path, year, month, day)
   # 文件路径
   word_name = os.path.exists(foldername)
   # 判断文件是否存在：不存在创建
   if not word_name:
       os.makedirs(foldername)
   return foldername


# 创建json文件
def CreateJson(JsonPath):
   if os.path.exists(JsonPath):
      with open(JsonPath, "r+") as f:
         f.seek(0)
         f.truncate()  # 清空文件
         print("Json file has been emptied ")
   else:
      with open(JsonPath, "w+") as f:
         print("Json file has been created")