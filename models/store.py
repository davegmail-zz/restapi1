from db import db

class StoreModel(db.Model):
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))
	#price = db.Column(db.Float(precision=2))

	items = db.relationship('ItemModel', lazy='dynamic') # sets many to one relationship (items to store), lazy makes it only execute when called

	def __init__(self, name):
		self.name = name
		#self.store_id = Store_id

	def json(self):
		# return the store and a list of all the items in that store (using the relationship defined above)
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # items.all() calls the db dynamically to create the item list

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()
		
	def save_to_db(self): # covers both insert and update
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

