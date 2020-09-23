
# regform and login form
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed

from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length




class NewPostForm(FlaskForm):

	
	blog_content = TextAreaField('Content',validators=[DataRequired()])
	media = FileField('media', validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Post')

