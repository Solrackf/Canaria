from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    caption = StringField('cation')
    images = HiddenField('images', validators=[DataRequired('Debes subir al menos una imagen')])
    submit = SubmitField('Publicar')

class CommentForm(FlaskForm):
    body = StringField('Comment')
    submit = SubmitField('Comentar')
