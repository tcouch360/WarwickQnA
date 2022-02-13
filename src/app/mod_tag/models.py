from app import db

"""This is the model for Tag class"""
class Tag(db.Model):
	__tablename__ = "tags"
	tag_id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String)
	question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))

	def __repr__(self):
		return '<Tag %r>' % (self.body)