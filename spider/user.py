# -*- coding: utf-8 -*-

'获取用户微博'

__author__ = 'zhang'

'''
根据uid，获取用户的信息
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import re
import request
from bs4 import BeautifulSoup
from html.parser import HTMLParser
html_parser = HTMLParser()

import utils
import json

import db

def get_userinfo(uid, html_txt='', soup=None):
	if not soup:
		soup = BeautifulSoup(html_parser.unescape(html_txt), 'html.parser')
	
	user_info = dict()

	# 选取用户信息模块
	its = soup.select('div.ut > span.ctt')

	user_info['uid'] = uid

	try:
		user_info['name'] = its[0].text.split('         ')[0].split(' ')[0]
		user_info['sex'] = its[0].text.split('         ')[0].split(' ')[1].split('/')[0]
		user_info['loc'] = its[0].text.split('         ')[0].split(' ')[1].split('/')[1]

		user_info['sign'] = its[1].text

		it = soup.find('div', class_='tip2')

		nums = utils.get_by_pattern(r'微博\[(\d+)\] 关注\[(\d+)\] 粉丝\[(\d+)\]', it.text)
	
		user_info['weibos_n'], user_info['follows_n'], user_info['fans_n']= nums[0]

		mp_it = soup.find('input', attrs={'name': 'mp', 'type': 'hidden'})
		if mp_it:
			user_info['mp'] = int(mp_it['value'])
		else:
			user_info['mp'] = 1
	except:
		print('获取用户信息出错！')
		return None
	return user_info

def get_weibo(uid, user_name, weibo_it):
	weibo = dict()
	try:
		weibo['id'] = weibo_it['id']
	
		nums = utils.get_by_pattern(r'赞\[(\d+)\] 转发\[(\d+)\] 评论\[(\d+)\]', weibo_it.text)
		weibo['atti_n'], weibo['repost_n'], weibo['comment_n'] = nums[0]

		weibo['text'] = weibo_it.text.split(' ')[0].split('​​​')[0]
		weibo['time'] = utils.time_format(weibo_it.text.split(' ')[-2].strip())
		weibo['device'] = weibo_it.text.split(' ')[-1].strip()

		# 获取微博评论
		weibo['comments'] = list()
		if int(weibo['comment_n'])>0:
			comment_url = 'http://weibo.cn/comment/%s' % weibo['id'][2:]
			comms_txt = request.req_get_with_auth(comment_url)

			com_soup = BeautifulSoup(html_parser.unescape(comms_txt.text), 'html.parser')

			# 查找其他用户
			user_adds(uid, comms_txt.text)

			for com_it in com_soup.find_all('div', class_='c', id=re.compile('^C_')):
				comment = dict()
				com_con = com_it.text.split(' ')[0].strip()
				comment['time'] = utils.time_format(com_it.text.split(' ')[-2].strip())
				comment['device'] = com_it.text.split(' ')[-1].strip()

				comment['to_name'] = user_name
				
				res_at_name = utils.get_by_pattern(r'回复@(.*?):', com_con)
				if len(res_at_name):
					comment['to_name'] = res_at_name[0].strip()
					com_con = ''.join(com_con.split('回复@%s:' % res_at_name[0]))
				comment['from_name'] = com_con.split(':')[0].strip()
				comment['text'] = ':'.join(com_con.split(':')[1:])
				weibo['comments'].append(comment)
	except Exception as e:
		print(e)
		print('获取微博信息出错！')
	if weibo.get('id', None) and weibo.get('text', None):
		return weibo
	else:
		return None

def user_adds(uid, html_txt):
	users_add = list()
	re_users = utils.get_by_pattern(r'<a href="/u/(\d+)"', html_parser.unescape(html_txt))
	for re_user in re_users:
		if re_user not in users_add and re_user != uid:
			users_add.append(re_user)
	db.userlist_adds(users_add)

def user_gets(uid, type_filter=1):
	print('正在抓取用户 %s 的微博...' % uid)
	user_url = 'http://weibo.cn/u/%s?filter=%d&page=' % (uid, type_filter)

	mp = -1
	np = 1

	user_info = dict()
	weibos = list()
	users_other = list()

	while (np<=mp or mp==-1):
		url = user_url + str(np)

		res = request.req_get_with_auth(url)

		soup = BeautifulSoup(html_parser.unescape(res.text), 'html.parser')
		user_adds(uid, res.text)

		if mp==-1:
			user_info = get_userinfo(uid, soup=soup)

			# 获取信息出错
			if not user_info:
				utils.need_sleep(3)
				print('抓取失败！')
				return None
			mp = user_info.get('mp', 1)
		
		for it in soup.find_all('div', class_='c', id=re.compile('^M_')):
			weibo = get_weibo(uid, user_info['name'], it)
			if weibo:
				weibos.append(weibo)

			utils.need_sleep(1)

		utils.need_sleep(2)
		np += 1
	
	# 写入数据
	with open(os.path.join(os.path.dirname(__file__), '../data/weibos_%s' % uid), 'w', encoding='utf-8') as fw:
		fw.write(json.dumps(weibos, ensure_ascii=False))
	with open(os.path.join(os.path.dirname(__file__), '../data/userinfo_%s' % uid), 'w', encoding='utf-8') as fw:
		fw.write(json.dumps(user_info, ensure_ascii=False))

	db.userlist_fin(uid)
	utils.need_sleep(3)

	print('抓取完成！')
  