from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from app_package.model import User,Post,Comment
from app_package import Bcrypt,db

from flask_login import login_user,logout_user,current_user,login_required
from app_package.users.utils import save_profile_pic,send_reset_mail
from app_package.users.forms import (registrationForm,loginForm,UpdateAccountForm,resetPasswordForm, requestPasswordResetForm)

comment = Blueprint('comment', __name__)


@comment.route('/newcomment', methods=['GET','POST'])
@login_required

def add_comment():

	post_id = request.form.get("post_id")

	post = Post.query.get(post_id)
	if post is None:
		abort(403)
	


	comment = request.form.get("comment")
	
	comment = Comment(comment=comment, post_id=post.id, author=current_user)
	db.session.add(comment)
	flash("post added",'success')
	db.session.commit()

	return redirect(url_for('posts.post',post_id=post_id))

