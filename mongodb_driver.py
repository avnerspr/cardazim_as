import sys
import os
from pymongo import MongoClient, errors
from pathlib import Path
from furl import furl

DEFULT_DB_NAME = 'card_database'
DEFULT_COLL_NAME = 'card_collection'
FIND_STANDART_PROJECTION = {'_id': False}

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

	def key_values(self, key: str):
		return self.coll.distinct(key)

	def creators(self):
		return  self.key_values('creator')

	def find_many(self, filter):
		docs = self.coll.find(filter, FIND_STANDART_PROJECTION)
		docs_list = list(docs)
		return docs_list

	def get_metadata(self, name: str, creator: str):
		return self.coll.find_one({'name': name, 'creator': creator}, FIND_STANDART_PROJECTION)



