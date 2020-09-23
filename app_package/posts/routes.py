

from app_package import Bcrypt,db,app
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from app_package.model import Post,Comment,User
from flask_login import current_user,login_required
from app_package.posts.forms import  NewPostForm
from app_package.users.utils import save_profile_pic
import secrets
import os
import base64


	        






posts =  Blueprint('posts', __name__)


def save_images(post_image):

	random_hex=secrets.token_hex(8)

	_,f_ext = os.path.splitext(post_image.filename)
	picture_name = random_hex + f_ext

	picture_path=os.path.join(app.root_path,'static/images',picture_name)
	image_size=(125,125)
	i=Image.open(post_image)
	i.thumbnail(image_size)
	
	i.save(picture_path)

	return picture_name



@posts.route('/newpost', methods=['GET','POST'])
@login_required
def newpost():
	form=NewPostForm()
	if form.validate_on_submit():
		if form.media.data:
			image_post=save_images(form.media.data)
			image_post = bytes(image_post,'utf-8')

			
			
			post = Post(blog_content=form.blog_content.data,
				 media=image_post ,user=current_user)
			db.session.add(post)
			

			db.session.commit()
		else:
		   post=Post(blog_content=form.blog_content.data,
			 user=current_user)
		   db.session.add(post)
		   db.session.commit()
		flash('posted success','success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html',title='New-Post', legend='Create New Post',form=form)




@posts.route('/post/<int:post_id>', methods=['GET'])

def post(post_id):

	post=Post.query.get(post_id)

	if post is None:
		abort(403)


	comments = Comment.query.order_by(Comment.timestamp.desc()).filter_by(post_id=post_id).all()
	return render_template('post.html', title='post' ,post=post, comments=comments)






@posts.route('/post/<int:post_id>/update', methods=['POST','GET'])
@login_required
def update_post(post_id):

	post=Post.query.get(post_id)

	if post.user != current_user:
	    abort(403)
	form=NewPostForm()
	if form.validate_on_submit():
		
		post.blog_content = form.blog_content.data
		db.session.commit()
		flash('post updated successfully','success')
		return redirect(url_for('posts.post',post_id=post.id))


	elif request.method=='GET':
		form.title.data= post.title
		form.blog_content.data=post.blog_content

	return render_template('create_post.html',title='New-Post', legend='Update post', form=form,post=post)




@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):

	post=Post.query.get(post_id)
	comment= Comment.query.filter_by(post_id=post_id).first()
	if post.user != current_user:
		abort(403)
	db.session.delete(post)
	if comment:
		db.session.delete(comment)
	db.session.commit()
	flash('post deleted successfully','success')
	return redirect(url_for('main.home'))


