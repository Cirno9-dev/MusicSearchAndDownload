# -*- coding: utf-8 -*-
import requests
import json
from urllib import parse
import base64
from Crypto.Cipher import AES
import sys
import re

Search_api='https://music.163.com/weapi/cloudsearch/get/web?csrf_token='

search_headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	'Referer':'https://music.163.com/search/',
	'Origin':'http://music.163.com',
	'Host':'music.163.com'
}

# 自己的网易云cookie
cookie = {
	'MUSIC_U' : ""
}

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"
#forth_param = "l6Brr86UeZ6C3Bsw"

def pkcs7padding(text):
	"""
	明文使用PKCS7填充
	最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
	:param text: 待加密内容(明文)
	:return:
	"""
	bs = AES.block_size  # 16
	length = len(text)
	bytes_length = len(bytes(text, encoding='utf-8'))
	# tips：utf-8编码时，英文占1个byte，而中文占3个byte
	padding_size = length if(bytes_length == length) else bytes_length
	padding = bs - padding_size % bs
	# tips：chr(padding)看与其它语言的约定，有的会使用'\0'
	padding_text = chr(padding) * padding
	return text + padding_text

def aes_en(text,key,iv):
	#print('pkcs7padding处理之前：',text)
	text =pkcs7padding(text)
	#print('pkcs7padding处理之后：',text)
	#entext = text + ('\0' * add)
	# 初始化加密器
	aes = AES.new(key.encode(encoding='utf-8'), AES.MODE_CBC, iv)
	enaes_text = str(base64.b64encode(aes.encrypt(str.encode(text))),encoding='utf-8')
	return enaes_text

def get_params(first_param):
	iv = b"0102030405060708"
	first_key = forth_param
	second_key = 16 * 'F'
	
	h_encText = aes_en(first_param, first_key, iv)
	h_encText = aes_en(h_encText, second_key, iv)
	return h_encText

if __name__ == "__main__":
	
	# search_name = '無間嫉妬劇場'
	search_name = "無間嫉妬劇場"
	page = 0
	try:
		# page = 0
		if page != 0:
			if_firstPage = "true"   #如果是第一页(即page=0)则if_firstPage为false，否则都为true
		else:
			if_firstPage = "false"   #page为0，这是评论第一页则if_firstPage为false
			
		first_param = "{\"hlpretag\":\"<span class=\\\"s-fc7\\\">\",\"hlposttag\":\"</span>\",\"s\":\"%s\",\"type\":\"1\",\"offset\":\"%s\",\"total\":\"%s\",\"limit\":\"20\",\"csrf_token\":\"\"}" %(search_name,str(page*20),if_firstPage)

		user_data = {
			'params': get_params(first_param),
			'encSecKey': "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
		}
	
		response = requests.post(Search_api,headers=search_headers,data=user_data,cookies=cookie)

		# json_dict = json.dumps(response.text, ensure_ascii=False)
		string = re.sub('\s', ' ', response.text)
		json_dict = json.loads(string)
		if json_dict['result']['songCount'] == 0:
			print("pageEnd")
			exit(0)
		songs = []
		for directory_temp in json_dict['result']['songs']:
			song = {}
			song["name"] = directory_temp['name'].replace("'", "")
			song["id"] = directory_temp['id']
			singers = ""
			for i in range(len(directory_temp['ar'])):
				singers += directory_temp['ar'][i]["name"]
				if i != len(directory_temp["ar"])-1:
					singers += "/"
			song["singers"] = singers.replace("'", "")
			songs.append(song)
		output = {"songs": songs}
		data = json.dumps(str(output).replace("'", "\""), ensure_ascii=False)
		#print(output["songs"][0])
		print(data)
	except Exception as e:
		print("error")
		print(e)
		#print(json_dict)