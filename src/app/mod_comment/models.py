from app import db

"""This is the model for Comment class"""
class Comment(db.Model):
	__tablename__ = "comments"
	comment_id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))
	answer_id = db.Column(db.Integer,db.ForeignKey('answers.answer_id'))
	upvotes = db.relationship('Upvote', backref = 'comment', lazy = 'dynamic')
	downvotes = db.relationship('Downvote', backref = 'comment', lazy = 'dynamic')

	def __repr__(self):
		return '<Comment %r>' % (self.body)