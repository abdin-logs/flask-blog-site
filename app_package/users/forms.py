# regform and login form

from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app_package.model import User
from flask_login import current_user



class registrationForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(),Length(min=2, max=20)])
	email = StringField('email', validators=[DataRequired(),Email()])
	

	password = PasswordField('password', validators=[DataRequired(),Length(min=6)])

	confirm_password=PasswordField('confrimPassword', validators=[DataRequired(),EqualTo('password')])
	
	submit=SubmitField('Sign Up')

	def validate_username(self,username):

		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username has been taken...try another!')

	def validate_email(self,email):

		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email has been taken...try another!')



class loginForm(FlaskForm):
	
	email = StringField('Email', validators=[DataRequired(),Email()])

	password = PasswordField('Password', validators=[DataRequired()])


	remember=BooleanField('Remember')
	login=SubmitField('Login')



class UpdateAccountForm(FlaskForm):

	username=StringField('Username',validators=[Length(min=2,max=20)])
	email=StringField('Email',validators=[Email()])
	upload_picture = FileField('Upload profile picture', validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Update')


	def validate_username(self,username):
		if username.data != current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('username exist try another')



	def validate_email(self,email):
		if email.data != current_user.email:
			user=User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email exist try another')
	
	
class requestPasswordResetForm(FlaskForm):

 	email= StringField('Email',validators=[DataRequired(),Email()])
 	submit=SubmitField('Submit')


 	def validate_email(self,email):
 		user=User.query.filter_by(email=email.data).first()
 		if user is None:
 			raise ValidationError('Email entered is invalid...try again')



class resetPasswordForm(FlaskForm):

    password = PasswordField('New password', validators=[DataRequired(),Length(min=6)])
    confirm_password=PasswordField('confrimPassword', validators=[DataRequired(),EqualTo('password')])	
    submit=SubmitField('Submit')