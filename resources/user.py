import sqlite3
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser() # this replaces the request.get_json() and parses the REST JSON Body to a list
	parser.add_argument('username',  # what is the structure of the body required to be passed in
		type=str,
		required=True,
		help="This Field is Required."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This Field is Required."
	)

	def post(self):
		# get the username and password from the JSON Body
		data = UserRegister.parser.parse_args() # class object (not self)
		# check to see if the user exists? access the db, see if user exists
		if UserModel.find_by_username(data['username']):
			return{"message": "A user with that name exists."}, 400

		user = UserModel(**data)
		user.save_to_db()
		
		return {"message": "User Created successfully."}, 201
