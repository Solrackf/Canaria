import os
from app.extinsions import db
from app.user import user
from app.user.models import User
from app.user.forms import SignupForm, LoginForm, ResetForm, PasswordResetForm, SettingForm
from app.helper.mail import send_email
from app.helper.pics import save_picture
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

basedir = os.path.abspath(os.path.dirname(__file__))

@user.route('/<username>')
def home(username):
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', user=user)

@user.route('un_follow/<username>')
def un_follow(username):
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.query.filter_by(username = username).first_or_404()
    if current_user.is_following(user):
        current_user.unfollow(user)
        flash(f'Has dejado de seguir a {user.username}', 'info')
    else :
        current_user.follow(user)
        flash(f'Has seguido a {user.username}', 'info')
    db.session.commit()
    return redirect(url_for('user.home', username = user.username))

@user.route('<username>/followers')
def user_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_users.html', users = user.all_followers)

@user.route('<username>/followed')
def user_followed(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_users.html', users = user.all_followed)

@user.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if not current_user.is_confirmed:
        flash("¿Este no es tu correo? Te invitamos a crea uno nuevo", "link")
        return redirect(url_for('main.home'))
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        if not current_user.email == form.email.data :
            current_user.email = form.email.data
            current_user.is_confirmed = False
        if form.avatar.data :
             f=form.avatar.data
             name = save_picture(f, os.path.join(basedir, 'static/images'))
             current_user.avatar = name
        flash(f'Tus datos han sido cambiados', 'success')
        db.session.commit()
        return redirect(url_for('user.home', username=current_user.username))
    form.username.data = current_user.username
    form.name.data = current_user.name
    form.email.data = current_user.email
    return render_template('setting.html', form=form)

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return 'debe cerrar la sesión para acceder a esta página'
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        user.self_follow
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Se ha creado una cuenta para { user.username } por favor, confirma tu cuenta', 'success')
        return redirect(url_for('user.confirm'))
    return render_template('signup.html', form=form)

@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'debe cerrar la sesión para acceder a esta página'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user and user.check_password(form.password.data) :
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login')) 

@user.route('/confirm')
@login_required
def confirm():
    if current_user.is_confirmed:
        flash("Se ha confirmado tu cuenta", "info")
        return redirect(url_for('main.home'))
    token = current_user.get_serializer_token(salt='Confirmación de correo')
    send_email(subject = 'Confirmación de correo',
               to = current_user.email,
               text_body = 'Si recibe esto, significa que no puede ver la página, comuníquese con el administrador.',
               template = 'confirm',
               token = token)
    flash(f'Se ha enviado un correo electrónico de confirmación a {current_user.email}, por favor confirma el correo', 'info')
    return redirect(url_for('main.home'))

@user.route('/confirm/<token>')
@login_required
def confirmation(token):
    if current_user.is_confirmed:
        flash("Tu cuenta está confirmada", "info")
        return redirect(url_for('main.home'))
    user = User.verify_serializer_token(token, salt='Confirmación de correo')
    if user:
        user.is_confirmed = True
        db.session.commit()
        flash(f'{user.username} Tú cuenta ha sido confirmada', 'success')
    else :
        flash(f"No se pudo confirmar su correo electrónico <a href={ url_for('user.confirm') }><b>Intentelo de nuevo</b></a>. Pedimos disculpas por las molestias.", 'danger')
    return redirect(url_for('main.home'))

@user.route('/reset', methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        flash("Necesita cerrar sesión para acceder a esta página", "warning")
        return redirect(url_for('main.home'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user :
            token = user.get_serializer_token(salt='restablecer contraseña')
            send_email(subject = 'restablecer contraseña',
                       to = user.email,
                       text_body = 'Si recibe esto, significa que no puede ver la página, comuníquese con el administrador.',
                       template = 'reset',
                       token = token)
            flash(f"Se ha enviado un correo a {user.email} para cambiar su contraseña", "info")
            return redirect(url_for('user.login'))
    return render_template('reset.html', form=form)

@user.route('reset/<token>', methods=['GET', 'POST'])
def reset_request(token):
    if current_user.is_authenticated:
        flash("Necesita cerrar sesión para acceder a esta página", "warning")
        return redirect(url_for('main.home'))
    form = PasswordResetForm()
    user = User.verify_serializer_token(token, salt='restablecer contraseña')
    if user:
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash("contraseña se ha restablecido. Iniciar sesión con nueva contraseña", "success")
            return redirect(url_for('user.login'))
        return render_template('password_reset.html', form=form)
    else :
        flash("Error al restablecer la contraseña, inténtalo de nuevo", "danger")
        return redirect(url_for('user.reset'))
    flash("Se ha enviado un correo de restablecimiento de contraseña, revise su bandeja de entrada", "info")
    return redirect(url_for('user.login'))
