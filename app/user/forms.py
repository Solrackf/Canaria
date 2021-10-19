from app.user.models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_login import current_user

class SignupForm(FlaskForm):
        name = StringField('name', validators=[DataRequired()])
        username = StringField('username', validators=[DataRequired()])
        email = EmailField('E-mail', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Registrarse')

        def validate_email(self, email):
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Este correo electrónico ya está en uso')

        def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Este usuario ya está en uso')

class LoginForm(FlaskForm):
        email = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Iniciar sesión')

        def validate_email(self, email):
            email = User.query.filter_by(email=email.data).first()
            if not email:
                raise ValidationError('La cuenta con este correo electrónico \'no existe')

class ResetForm(FlaskForm):
        username = StringField('username', validators=[DataRequired()])
        submit = SubmitField('Enviar correo')

        def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if not user:
                raise ValidationError('No se pudo\'encontrar una cuenta con este nombre de usuario')

class PasswordResetForm(FlaskForm):
        password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas no coinciden')])
        confirm  = PasswordField('Repetir contraseña')
        submit = SubmitField('Cambiar contraseña')

class SettingForm(FlaskForm):
        avatar = FileField('Avatar', validators=[FileAllowed(['jpg','png'])])
        name = StringField('name')
        username = StringField('username')
        email = EmailField('E-mail', validators=[Email()])
        submit = SubmitField('Guardar')

        def validate_email(self, email):
            if email.data != current_user.email:
                email = User.query.filter_by(email=email.data).first()
                if email:
                    raise ValidationError('Este correo electrónico ya está en uso')

        def validate_username(self, username):
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('Este usuario ya está en uso')

