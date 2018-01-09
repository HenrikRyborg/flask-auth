from flask import flash, redirect, render_template, url_for

from . import auth
from .forms import registerAccountForm, loginForm 
from .. import db
# from ..models import 

@auth.route('/registerAccount', methods=['GET', 'POST'])
def registerAccountView():
    form = registerAccountForm()
    
    return render_template('auth/registerAccount.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def loginView():
    form = loginForm()
    
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
def logoutView():
    flash('You have successfully been logged out.')

    return redirect(url_for('auth.loginView'))