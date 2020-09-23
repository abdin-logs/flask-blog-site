import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
from flask_mail import Mail
from app_package.config import config
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager




app = Flask(__name__)

app.config.from_object(config)


db = SQLAlchemy(app)
Bcrypt = Bcrypt(app)


migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

LoginManager=LoginManager(app)
LoginManager.login_view='users.login'

mail=Mail(app)


from app_package.users.routes import users 
from app_package.main.routes import main
from app_package.posts.routes import posts
from app_package.comments.routes import comment
from app_package.errors.handlers import errors



app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(comment)
app.register_blueprint(errors)
