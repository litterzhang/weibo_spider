# -*- coding: utf-8 -*-

'爬虫主程序'

__author__ = 'zhang'

from spider import user

import db

if __name__=='__main__':
	while True:
		uid = db.userlist_get()
		if not uid:
			break
		user.user_gets(uid)