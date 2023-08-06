#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
class Mongo(object):
	def __init__(self, host='localhost', port=27017):
		self._client = MongoClient(host, port)

	#用户的mongo
	def getUserCollection(self):
		db = self._client.lab_user
		db.authenticate("user", "password")
		collection = db.user
		return collection


