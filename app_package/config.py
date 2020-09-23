
import os
class config():

	SECRET_KEY= 'f0db1cf00be92e4e76d02161a2152f6b'
	SQLALCHEMY_DATABASE_URI= 'postgres+psycopg2://postgres:abdin5817@localhost/wajirlive'
	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT=587
	MAIL_USE_TLS=True
	MAIL_USERNAME=os.environ.get('EMAIL-USER')
	MAIL_PASSWORD=os.environ.get('EMAIL-PASS')
	