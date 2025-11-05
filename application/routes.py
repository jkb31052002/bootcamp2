from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from flask import current_app as app

from datetime import datetime, date

from .models import *

#HOME ROUTE
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        pwd = request.form.get('pwd')

        this_admin = Admin.query.filter_by(username=u_name).first()

        if not this_admin:
            return render_template('admin_login.html', error="User not found")
        if this_admin.password != pwd:
            return render_template('admin_login.html', error="Incorrect password")
        
        login_user(this_admin)

        #add dashboard functionalities

        return render_template('admin_dashboard.html', current_user=this_admin, u_name=u_name)
    return render_template('admin_login.html')


#SPONSOR REGISTRATION ROUTE
@app.route('/sponsorregister', methods=['GET', 'POST'])
def sponsorregister():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        pwd = request.form.get('pwd')
        c_name = request.form.get('c_name')
        c_budget = request.form.get('c_budget')
        industry = request.form.get('industry')

        this_sponsor = Sponsor.query.filter_by(username=u_name).first()
        if this_sponsor:
            return render_template('sponsor_register.html', error="Username already exists")
        
        user = User(username=u_name, user_role='1')
        db.session.add(user)
        db.session.commit()

        sponsor = Sponsor(username=u_name, password=pwd, company_name=c_name, company_budget=c_budget, industry=industry, sponsor_id=user.id)
        db.session.add(sponsor)
        db.session.commit()

        return redirect('/sponsorlogin')
    return render_template('sponsor_register.html')


#SPONSOR LOGIN ROUTE
@app.route('/sponsorlogin', methods=['GET', 'POST'])
def sponsorlogin():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        pwd = request.form.get('pwd')

        this_sponsor = User.query.filter_by(username=u_name).first()
        if not this_sponsor:
            return render_template('sponsor_login.html', error="User not found")
        
        if this_sponsor:
            sponsor = Sponsor.query.filter_by(sponsor_id=this_sponsor.id).first()
            if sponsor.password != pwd:
                return render_template('sponsor_login.html', error="Incorrect password")
            
            else:
                if sponsor.flagged == 1:
                    return render_template('sponsor_login.html', error="Your account has been flagged. Please contact support.")
                
                else:
                    if this_sponsor.user_role != '1':
                        return render_template('sponsor_login.html', error="Invalid user role for sponsor login.")
                    else:
                        this_sponsor = sponsor
                        login_user(sponsor)
                        return render_template('sponsor_dashboard.html', current_user=sponsor, u_name=u_name)
    return render_template('sponsor_login.html')