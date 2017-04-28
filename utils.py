# -*- coding: utf-8 -*-

'辅助小工具类'

__author__ = 'zhang'

import time
import datetime

import re
import random

def time_now():
	return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def time_format(t_str):
	try:
		t_d = t_str.split()[0].strip()
		t_t = t_str.split()[1].strip()

		t = dict()

		if t_d=='今天':
			d = datetime.date.today()
			t['y'] = int(str(d).split('-')[0])
			t['m'] = int(str(d).split('-')[1])
			t['d'] = int(str(d).split('-')[2])
		elif t_d=='昨天':
			d = datetime.date.today() - datetime.timedelta(days=1)
			t['y'] = int(str(d).split('-')[0])
			t['m'] = int(str(d).split('-')[1])
			t['d'] = int(str(d).split('-')[2])
		else:
			if len(t_d.split('年'))>=2:
				t['y'] = int(t_d.split('年')[0])
				t_d = t_d.split('年')[1]
			else:
				t['y'] = int(str(datetime.date.today()).split('-')[0])
			
			t['m'] = int(t_d.split('月')[0])
			t_d = t_d.split('月')[1]
			t['d'] = int(t_d.split('日')[0])
			
		t['h'] = int(t_t.split(':')[0])
		t['M'] = int(t_t.split(':')[1])

		return '%04d-%02d-%02d %02d:%02d' % (t['y'], t['m'], t['d'], t['h'], t['M'])
	except:
		return ''

def get_by_pattern(pattern, text):
	return re.findall(pattern, text, re.S)

def need_sleep(t):
	if t == 1:
		print('正在进行休眠...预计1.5秒')
		time.sleep(1.0 + random.random())
		print('休眠结束！')
	if t == 2:
		print('正在进行休眠...预计7.5秒')
		time.sleep(5.0 + 5.0*random.random())
		print('休眠结束！')
	if t == 3:
		print('正在进行休眠...预计90秒')
		time.sleep(60.0 + 60.0*random.random())
		print('休眠结束！')
