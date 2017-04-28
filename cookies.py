# -*- coding: utf-8 -*-

'模拟登录获取cookies'

__author__ = 'zhang'

'''
Required
- requests (必须)
考虑到 weibo.cn 变态的验证码，放弃这种浪费生命的方式吧，
2016.4.8
'''

import json
import requests
import re
from urllib.parse import urljoin
from html.parser import HTMLParser
html_parser = HTMLParser()

import db

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

headers = {
	'User-Agent': agent,
	'Host': 'weibo.cn',
	'Origin': 'https://login.weibo.cn',
	'Referer': 'https://login.weibo.cn/login/'
}

session = requests.session()

url_login = 'https://weibo.cn/login/'
 
def get_params(url_login):
	print('正在获取登录参数...')

	html = session.get(url_login, headers=headers)

	html.encoding = 'utf-8'

	pattern = r'action="(.*?)".*?type="password" name="(.*?)".*?name="vk" value="(.*?)".*?name="capId" value="(.*?)"'
	res = re.findall(pattern, html_parser.unescape(html.text), re.S)
	
	if res == []:
		raise Exception('你的网络有问题，请检查网络后重试！')
	else:
		print('成功获取登录参数！')
		return res[0]

def get_cha(capId):
	print('正在下载登录验证码...')
	cha_url = 'http://weibo.cn/interface/f/ttt/captcha/show.php?cpt=%s' % capId
	cha = session.get(cha_url, headers=headers)
	with open('cha.jpg', 'wb') as f:
		f.write(cha.content)
		f.close()

	print('成功下载验证码!请到当前目录下寻找 cha.jpg 查看验证码')
	cha_code = input('请输入验证码:')

	return cha_code

def get_cookies(mobile, password, cha_code, post_url, password_f, vk, capId):
	print('正在尝试登录请求...')
	postdata = {
		'mobile': mobile,
		'code': cha_code,
		'remember': 'on',
		'backURL': 'http://weibo.cn',
		'backTitle': '微博',
		'tryCount': '',
		'vk': vk,
		'capId': capId,
		'submit': '登录',
	}
	postdata[password_f] = password
	post_url = urljoin(url_login, post_url)

	page = session.post(post_url, data=postdata, headers=headers)

	pattern = r'<div class="me">(.*?)</div>'
	res = re.findall(pattern, html_parser.unescape(page.text), re.S)

	if res == []:
		raise Exception('你的网络有问题，请检查网络后重试！')
	elif res[0] != '您请求的页面不存在':
		raise Exception('登录失败 %s' % res[0])
	else:
		cookies = requests.utils.dict_from_cookiejar(session.cookies)
		print('登录成功！')
		return cookies

def login():
	try:
		post_url, password_f, vk, capId = get_params(url_login)

		cha_code = get_cha(capId)

		mobile = input('请输入微博登录账户:')
		password = input('请输入微博登录密码:')

		cookies = get_cookies(mobile, password, cha_code, post_url, password_f, vk, capId)

		db.account_add(mobile, password, json.dumps(cookies, ensure_ascii=False))

	except Exception as e:
		print(e)

if __name__ == "__main__":
	login()
	