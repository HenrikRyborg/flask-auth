from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from . import auth
from .forms import registerAccountForm, loginForm 
from .. import db
from ..models import accountUser, user, account
# from ..models import 

@auth.route('/registerAccount', methods=['GET', 'POST'])
def registerAccountView():
    form = registerAccountForm()
    
    return render_template('auth/registerAccount.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def loginView():
    if current_user.is_authenticated:
        return redirect(url_for('indexBP.indexView'))
    form = loginForm()
    if form.validate_on_submit():
        acc = account.query.filter_by(name=form.accountName.data).first()
        usr = user.query.filter_by(email=form.email.data).first()
        accUsr = accountUser.query.filter_by(accountID=acc.id,
                                             userID=usr.id,).first()
        if accUsr is None or not accUsr.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.loginView'))

        login_user(accUsr)
        return redirect(url_for('indexBP.indexView'))                                             
    
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
def logoutView():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('indexBP.indexView'))