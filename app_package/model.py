
from datetime import datetime
from flask import flash
from app_package import db,LoginManager
from flask_login import  UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app_package import app
import psycopg2





@LoginManager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))


#folower and followed table

followers = db.Table(
   'followers',
   db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
   db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))


	)


#db table for users
class User(db.Model,UserMixin):
	id = db.Column(db.Integer, nullable = False , primary_key =True)
	username = db.Column(db.String(20),nullable=False, unique=True)
	email = db.Column(db.String(60), nullable=False,unique=True)
	image_file=db.Column(db.String(60),nullable=False,default="default.png")
	password = db.Column(db.String(60), nullable= False)
	posts = db.relationship('Post',backref='user', lazy=True)
	comments = db.relationship('Comment', backref='author', lazy=True)
	followed= db.relationship(
		'User' , secondary = followers, 
		primaryjoin=( followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref= db.backref('followers', lazy='dynamic'), lazy='dynamic')


	def follow(self,user):
		if not self.is_following(user):
		 self.followed.append(user)


	def unfollow(self,user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self,user):
		return self.followed.filter(followers.c.followed_id==user.id).count()>0

	def post_followed(self):
		return Post.query.join(followers,(followers.c.followed_id==post.user_id).
		       filter(followers.c.follower_id==self.id).order_by(Post.date_posted.desc()))

	

	def get_reset_token(self,expire_time=1800):
		
			s = Serializer(app.config['SECRET_KEY'],expire_time)
			return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
			s=Serializer(app.config['SECRET_KEY'])
			try:
				user_id=s.loads(token)['user_id']
			except:
				 return None
			return User.query.get(user_id)


	def __repr__(self):

		return f"User('{self.username}', '{self.email}' )"


class Post(db.Model):
	id = db.Column(db.Integer, nullable= False , primary_key =True)
	date_posted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	blog_content= db.Column(db.Text, nullable= False)
	media = db.Column(db.LargeBinary,nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable= False )
	post_comments = db.relationship('Comment',backref='post', lazy=True)


	

	def __repr__(self):

		return f"User('{self.title},' {self.date_posted}' )"



class Comment(db.Model):
	id = db.Column(db.Integer, nullable= False , primary_key =True)
	timestamp=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	comment= db.Column(db.Text, nullable= False)
	
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable= False )
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable= False )

	def __repr__(self):

		return f"Comment('{self.comment},' {self.timestamp}' )"