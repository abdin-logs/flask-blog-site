

import os
from flask import url_for
import secrets
from app_package import mail,app
from flask_mail import  Message
from PIL import Image


def save_profile_pic(form_picture):

	random_hex=secrets.token_hex(8)

	_,f_ext = os.path.splitext(form_picture.filename)

	picture_name = random_hex + f_ext

	picture_path=os.path.join(app.root_path,'static/images',picture_name)
	image_size=(125, 125)
	i=Image.open(form_picture)
	i.thumbnail(image_size)
	i.save(picture_path)

	return picture_name



def send_reset_mail(user):

	
	token = user.get_reset_token()

	msg=Message('password reset request', sender='MAIL_USERNAME', recipients=[user.email])

	msg.body =  f''' Please click on the link bellow to reset your password
	              {url_for('users.reset_password', token = token, _external=True)}
	              if you did not request reset password please contact 
	'''
	mail.send(msg)

