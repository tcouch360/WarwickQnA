from flask import render_template, g, Blueprint
from flask_login import current_user
from app import app, db
from ..forms import TagForm
from app.mod_user.models import User
from app.mod_question.models import Question
from app.mod_vote.models import Upvote, Downvote
from app.mod_comment.models import Comment
from app.mod_tag.models import Tag
from datetime import datetime
from sqlalchemy import and_
mod_tag = Blueprint('mod_tag', __name__)

@mod_tag.route('/searchByTags', methods = ['GET', 'POST'])
def searchByTags():
	"""search question by tags in question database"""
	form = TagForm()
	if form.validate_on_submit():
		tag_data = form.tag.data
		tag_data = tag_data.split(',')
		tags = Tag.query.filter(Tag.body.in_(tag_data)).all()
		tag_id=[]
		for tag in tags:
			tag_id.append(tag.question_id)
		questions = Question.query.filter(Question.question_id.in_(tag_id)).order_by(Question.timestamp.desc()).all()
		return render_template('mod_tag/searchByTags.html', form = form, questions = questions, title = 'Search By Tags')
	return render_template('mod_tag/searchByTags.html',form = form, questions = [], title = 'Search By Tags')

"""Registers a function to run before each request.The function will be called without any arguments. 
   If the function returns a non-None value, it’s handled as if it was the return value from the view and further request handling is stopped"""

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

"""app.context-> Binds the application only. For as long as the application is bound to the current context the flask.current_app points to that application. 
				 An application context is automatically created when a request context is pushed if necessary.
				 """
"""context_processor:Registers a template context processor function."""
@app.context_processor
def utility_processor():
	def user(user_id):
		"""filters users by user_id and returns an object of users"""
		return User.query.filter_by(user_id = user_id).first()
	return dict(user = user)

@app.context_processor
def answer_comments():
	def get_answer_comments(answer_id):
		"""filters answers by anser_id and returns an object of comments filtered"""
		return Comment.query.filter_by(answer_id = answer_id).all()
	return dict(get_answer_comments = get_answer_comments)

@app.context_processor
def answer_id():
	def create_answer_id(answer_id):
		return "add-answer-comment-" + str(answer_id)
	return dict(create_answer_id = create_answer_id)

@app.context_processor
def body_id():
	def create_comment_body_id(answer_id):
		return "comment-body-" + str(answer_id)
	return dict(create_comment_body_id = create_comment_body_id)

"""tells number of votes based on whether it is upvote,downvote on question or answer"""
@app.context_processor
def vote_check():
	def vote_allowed_check(pid, votetype, contenttype):
		ans = 1
		if g.user.is_authenticated:
			if votetype == 1:
				"""Votetype 1-> Upvote"""
				if contenttype == 1:
					"""Upvote on a question"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.question_id == pid)).all())
				elif contenttype == 2:
					"""Upvote on an answer"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.answer_id == pid)).all())
				else :
					"""Upvote on a comment"""
					ans = len(Upvote.query.filter(and_(Upvote.user_id == g.user.user_id, Upvote.comment_id == pid)).all())
			else : 
				"""Votetype 2->Downvote"""
				if contenttype == 1:
					"""Downvote on a question"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.question_id == pid)).all())
				elif contenttype == 2:
					"""Downvote on an answer"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.answer_id == pid)).all())
				else :
					"""Downvote on a comment"""
					ans = len(Downvote.query.filter(and_(Downvote.user_id == g.user.user_id, Downvote.comment_id == pid)).all())
			print (ans)
		if ans >= 1:
			return 0
		else :
			return 1
	return dict(vote_allowed_check = vote_allowed_check)