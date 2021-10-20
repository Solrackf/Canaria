from secrets import token_hex
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or token_hex(16)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///../Database/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER= 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'login.zroot@gmail.com'
MAIL_PASSWORD = '#L0g1nzr00t'
MAIL_SUBJECT_PREFIX = 'Serinus Canaria : '
MAIL_DEFAULT_SENDER = 'Drac de Serinus'
DROPZONE_DEFAULT_MESSAGE = 'Suelte o haga clic para subir una imagen <br> (se pueden cargar 3 archivos como máximo)'
DROPZONE_ALLOWED_FILE_TYPE='image'
DROPZONE_MAX_FILE_SIZE=5
DROPZONE_MAX_FILES=3
DROPZONE_UPLOAD_ON_CLICK=True
DROPZONE_IN_FORM=True
DROPZONE_ENABLE_CSRF=True
DROPZONE_UPLOAD_MULTIPLE=True
DROPZONE_PARALLEL_UPLOADS=3
DROPZONE_UPLOAD_BTN_ID='submit'
DROPZONE_UPLOAD_ACTION='post.upload_image'
ALLOWED_HOSTS = [".herokuapp.com", ".serinus.herokuapp.com"]
WTF_CSRF_ENABLED=False