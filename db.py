# -*- coding: utf-8 -*-

'TinyDb数据库支持'

__author__ = 'zhang'

import utils

from tinydb import TinyDB, Query

import os
db = TinyDB(os.path.join(os.path.dirname(__file__), 'db.json'))

def account_add(mobile, password, cookie):
	acc_tab = db.table('accounts')

	if account_sea(mobile):
		account_del(mobile)
	acc_tab.insert({'mobile': mobile, 'password': password, 'cookie': cookie, 'time': utils.time_now()})

def account_del(mobile):
	ACC = Query()
	acc_tab = db.table('accounts')

	acc_tab.remove(ACC.mobile == mobile)

def account_sea(mobile):
	ACC = Query()
	acc_tab = db.table('accounts')

	res = acc_tab.search(ACC.mobile == mobile)

	if len(res):
		return res[0]
	return None

def account_gets():
	acc_tab = db.table('accounts')

	return acc_tab.all()

def userlist_sea(uid):
	UL = Query()
	ul_tab = db.table('userlist')

	res = ul_tab.search(UL.uid == uid)

	if len(res):
		return res[0]
	return None

def userlist_add(uid):
	ul_tab = db.table('userlist')

	if not userlist_sea(uid):
		ul_tab.insert({'uid': uid, 'finish': False})

def userlist_adds(uids):
	for uid in uids:
		userlist_add(uid)

def userlist_del(uid):
	UL = Query()
	ul_tab = db.table('userlist')

	res = ul_tab.remove(UL.uid == uid)

def userlist_fin(uid):
	ul_tab = db.table('userlist')

	userlist_del(uid)
	ul_tab.insert({'uid': uid, 'finish': True})

def userlist_get():
	UL = Query()
	ul_tab = db.table('userlist')

	us = ul_tab.search(UL.finish == False)
	if len(us):
		return us[0]['uid']
	return None