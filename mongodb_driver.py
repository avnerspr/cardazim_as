import sys
import os
from pymongo import MongoClient, errors
from pathlib import Path
from furl import furl

DEFULT_DB_NAME = 'defult_database'
DEFULT_COLL_NAME = 'defult_collection'

class MongoDB_Driver:

	def __init__(self, client, db, coll):
		'''
		method not meant for direct accsess. because constractor does not create a mongoDB client, database, collection
		'''
		self.client = client
		self.db = db
		self.coll = coll

	@classmethod
	def create(cls, host='local_host', port=27017, db_name=DEFULT_DB_NAME, coll_name=DEFULT_COLL_NAME):
		client = MongoClient(host, port)
		db = client[db_name]
		coll = db[coll_name]
		return MongoDB_Driver(client, db, coll)

	@classmethod
	def create_from_url(cls, url): 
		'''
		create driver from url representing the driver
		'''
		url = furl(url)
		db_name, coll_name = url.args.get('database_name', DEFULT_DB_NAME), url.args.get('collection_name',DEFULT_COLL_NAME)
		return MongoDB_Driver.create(url.host, url.port, db_name, coll_name)


	def upsert(self, metadata):

		if 'name' not in metadata.keys() or self.coll.find_one({'name': metadata['name']}) == None:
			self.coll.insert_one(metadata)
		else:
			self.coll.replace_one({'name': metadata['name']}, metadata)


