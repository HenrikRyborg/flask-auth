from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
import uuid

from . import auth
from .forms import registerAccountForm, loginForm, changePasswordForm
from .. import db
from ..models import accountUser, user, account
# from ..models import 

@auth.route('/registerAccount', methods=['GET', 'POST'])
def registerAccountView():
    form = registerAccountForm()
    if form.validate_on_submit():            
        
        acc = account.query.filter_by(name=form.accountName.data).first()        
        if not acc:
            acc = account(name=form.accountName.data)
            db.session.add(acc)
            usr = user.query.filter_by(email=form.email.data).first()
            if not usr:
                usr = user(email=form.email.data)
                db.session.add(usr)  

            usr = user.query.filter_by(email=form.email.data).first()
            acc = account.query.filter_by(name=form.accountName.data).first()
            accUsr = accountUser(accountID=acc.id,
                                 userID=usr.id,
                                 password=form.password.data,
                                 isAdmin = True,
                                 isWriter = True,
                                 uuid=str(uuid.uuid4()))
            db.session.add(accUsr)
            db.session.commit()
            flash('Account successfully created, please log in')
            return redirect(url_for('auth.loginView'))                                 
        else:
            flash('Account already in use')
    
    return render_template('auth/registerAccount.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def loginView():
    if current_user.is_authenticated:
        return redirect(url_for('indexBP.indexView'))

    if not current_user.isValidated:
        flash('Please validate your account')

    if current_user.isDeactivated:
        flash('Your user account has been deactivated, please contact your local administrator.')

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

@auth.route('/changePassword')
def changePasswordView():
    form = changePasswordForm()
    return render_template('auth/changePassword.html', form=form)

@auth.route('/logout')
def logoutView():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('indexBP.indexView'))