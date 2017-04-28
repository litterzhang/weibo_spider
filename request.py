# -*- coding: utf-8 -*-

'自定义请求'

__author__ = 'zhang'

import requests
import json

import db

# agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

# headers = {
# 	'User-Agent': agent,
# 	'Host': 'weibo.cn',
# 	'Origin': 'https://login.weibo.cn',
# 	'Referer': 'https://login.weibo.cn/login/'
# }

def init_headers():
	headers = requests.utils.default_headers()
	user_agent = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0'
	}
	headers.update(user_agent)
	return headers

headers = init_headers()

session = requests.session()
used_cookies = list()

def get_cookie():
	accs = db.account_gets()
	if len(accs):
		for acc in accs:
			cookie = acc.get('cookie', None)
			if cookie not in used_cookies:
				return json.loads(cookie), cookie
	return None, None

auth_cookies, auth_cookies_str = get_cookie()

def req_get_with_auth(url, session=session, cookies=auth_cookies, headers=headers):
	global auth_cookies, auth_cookies_str
	if not auth_cookies:
		raise Exception('没有可用的账号！')
	try:
		res = session.get(url, cookies=auth_cookies, headers=headers)

		return res
	except:
		print('正在更换cookies...')
		used_cookies.append(auth_cookies_str)
		auth_cookies, auth_cookies_str = get_cookie()
		print('更换完毕！')
		req_get_with_auth(url, session=session, cookies=auth_cookies, headers=headers)

