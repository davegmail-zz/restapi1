import sqlite3
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser() # this replaces the request.get_json() and parses the REST JSON Body to a list
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank!"
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id!"
	)

	@jwt_required() # authorized user token required
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), 200 
		return {'message': 'Item not found'}, 404

	def post(self, name):
		# check the named item if it exists in the db
		if ItemModel.find_by_name(name):
			return {'message': "An item with the name %r already exists." % name}, 400
		data = Item.parser.parse_args() # class object (not self)

		#item = {'name': name, 'price': data['price']}
		item = ItemModel(name, data['price'], data['store_id'])

		try:
			item.save_to_db()
		except:
			return {'message': "An error occured when inserting and item."}, 500
		return item.json(), 201

	def put(self, name):
		data = Item.parser.parse_args() # class object (not self) - parse the JSON body
		item = ItemModel.find_by_name(name)

		if item is None:  # if item does not exist create it
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']
		item.save_to_db()
		return item.json()

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted.'}


class ItemList(Resource):
	def get(self):
		# return a list of items in JSON
		return {'items': [item.json() for item in ItemModel.query.all()]}

