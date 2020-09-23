
from flask import render_template,url_for,flash,redirect,request,Blueprint
from app_package.model import User,Post
from app_package import Bcrypt,db
from flask_login import login_user,logout_user,current_user,login_required
from app_package.users.utils import save_profile_pic,send_reset_mail
from app_package.users.forms import (registrationForm,loginForm,UpdateAccountForm,resetPasswordForm, requestPasswordResetForm)

users =  Blueprint('users', __name__)


@users.route("/register",methods=['GET','POST'])
def register():
		
		form=registrationForm()
		if form.validate_on_submit():
				hash_password=Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
				user=User(username=form.username.data,email=form.email.data,password=hash_password)
				db.session.add(user)
				db.session.commit()
				flash('Your account has been created!','success')
				return redirect(url_for('users.login'))

		return  render_template('register.html', title="register", form=form)




@users.route('/login', methods=['GET','POST'])

def login():
		
		form=loginForm()
		if form.validate_on_submit():
				user=User.query.filter_by(email=form.email.data).first()
				if user and Bcrypt.check_password_hash(user.password,form.password.data):
						login_user(user,remember=form.remember.data)
						return redirect(url_for('main.home'))
				else:
						flash('The email and password that you entered did not match our records. Please double-check and try again','danger')

		return render_template('login.html', title="login",form=form)


@users.route('/logout')

def logout():
		 logout_user()
		 return redirect(url_for('users.login'))





@users.route('/user/<username>', methods=['POST','GET'])
@login_required
def account(username):
		form = UpdateAccountForm()
		
		user = User.query.filter_by(username=username).first_or_404()
		
		
		image_file = url_for('static', filename='images/' + user.image_file)

		return render_template('account.html',title='user/profile', user=user ,image_file = image_file,form=form)


@users.route('/edit', methods=['POST','GET'])
@login_required
def edit_info():

		form = UpdateAccountForm()	

		if form.validate_on_submit():
			
			if form.upload_picture.data:
					profile_picture=save_profile_pic(form.upload_picture.data)
					current_user.image_file=profile_picture
			current_user.username = form.username.data
			current_user.email= form.email.data
			db.session.commit()
			flash('Your profile has been updated','info')

			return redirect(url_for('users.edit_info'))
			
			
		elif request.method == 'GET':
				form.username.data=current_user.username
				form.email.data=current_user.email
		#image_file = url_for('static', filename='images/' + user.image_file)
		
		
		return render_template('edit_profile.html', form=form)


@users.route("/user_post/<string:username>")

def user_post(username):

		page=request.args.get('page',1, type=int)
		user = User.query.filter_by(username=username).first_or_404()
		
		posts=Post.query.filter_by(user=user).order_by(Post.date_posted.desc()).paginate( page=page, per_page=5)
		return  render_template('user_post.html', posts = posts,user=user)


@users.route('/request_password', methods=['GET','POST'])
def request_password():
		if current_user.is_authenticated:
				return redirect(url_for('main.home'))

		form=requestPasswordResetForm()
		if form.validate_on_submit():
				user= User.query.filter_by(email=form.email.data).first()
				send_reset_mail(user)
				flash('An email to reset password is sent to your email ', 'info')
				return redirect(url_for('users.login'))
		return  render_template('request_password.html', title=' reset request',form=form)


 
@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
				if current_user.is_authenticated:
						return redirect(url_for('main.home'))
				user=User.verify_token(token)
				if user is None:
					flash('invalid or expired url','warning')
					return redirect(url_for('users.request_password'))
				form = resetPasswordForm()
				if form.validate_on_submit():
						hash_password=Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
						user.password=hash_password
						db.session.commit()
						flash('Your password has been reseted','success')
						return redirect(url_for('users.login'))
				return  render_template('reset_password.html', form=form, title='reset password')



@users.route('/follow/<username>')
@login_required
def follow(username):
		user = User.query.filter_by(username=username).first()

		if user is None :
				flash('User {} not found'.format(username))
				return redirect(url_for('main.home',username=username))

		if user == current_user:
			flash('you cannot follow yourself')
			return redirect(url_for('users.account',username=username))

		current_user.follow(user)
		db.session.commit()
		flash('you are now following {}'.format(username))
		return redirect(url_for('users.account',username=username))
 
@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user= User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found'.format(username))
		return redirect(url_for('main.home',username=username))
	if user == current_user:
		flash('you cannot unfollow yourself')
		return redirect(url_for('users.account',username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('you are not following {}'.format(username))
	return redirect(url_for('users.account',username=username))


 