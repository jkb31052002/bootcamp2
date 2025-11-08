from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

from flask import current_app as app

from datetime import datetime, date

from .models import *


def calculate_campaign_progress(start_date, end_date):
    current_date = date.today()
    total_days = (end_date - start_date).days
    elapsed_days = (current_date - start_date).days
    if total_days > 0:
        progress = (elapsed_days / total_days) * 100
    else:
        progress = 0
    return round(progress, 2)

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


#SPONSOR CREATE CAMPAIGN ROUTE
@app.route('/create_campaign', methods=['GET', 'POST'])
@login_required
def create_campaign():
    # this_sponsor = Sponsor.query.filter_by(sponsor_id=current_user.id).first()
    # if not this_sponsor:
    #     return redirect('/sponsorlogin')

    # this_id = current_user.id
    # if this_id.user_role != '1':
    #     return redirect('/sponsorlogin', error = "Unauthorized access to create campaign.")
    
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        budget = request.form.get('budget')
        # if budget <= 0:
        #     return render_template('create_campaign.html', error="Budget must be greater than 0")
        niche = request.form.get('niche')
        sdate = request.form.get('sdate')
        sdate = datetime.strptime(sdate, '%Y-%m-%d').date()
        edate = request.form.get('edate')
        edate = datetime.strptime(edate, '%Y-%m-%d').date()
        current_date = date.today()
        if edate < sdate:
            return render_template('create_campaign.html', error="End date must be after start date")
        if sdate < current_date:
            return render_template('create_campaign.html', error="Start date must be today or later")
        
        visibility = request.form.get('visibility')
        goals = request.form.get('goals')
        this_id = current_user.id
        sponsor = Sponsor.query.filter_by(sponsor_id=this_id).first()

        new_campaign = Campaign(name=name, description=desc, campaign_budget=budget, start_date=sdate, end_date=edate, visibility=visibility, goals=goals, niche=niche, sponsor_id=current_user.id)
        db.session.add(new_campaign)
        db.session.commit()

        return redirect('/sponsor_campaign')
    return render_template('create_campaign.html')



#SPONSOR EDIT CAMPAIGN ROUTE
@app.route('/edit_campaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        budget = request.form.get('budget')
        # if budget <= 0:
        #     return render_template('create_campaign.html', error="Budget must be greater than 0")
        niche = request.form.get('niche')
        sdate = request.form.get('sdate')
        sdate = datetime.strptime(sdate, '%Y-%m-%d').date()
        edate = request.form.get('edate')
        edate = datetime.strptime(edate, '%Y-%m-%d').date()
        current_date = date.today()
        if edate < sdate:
            return render_template('create_campaign.html', error="End date must be after start date")
        if sdate < current_date:
            return render_template('create_campaign.html', error="Start date must be today or later")
        
        visibility = request.form.get('visibility')
        goals = request.form.get('goals')


        campaign.name = name
        campaign.description = desc
        campaign.campaign_budget = budget
        campaign.start_date = sdate
        campaign.end_date = edate
        campaign.visibility = visibility
        campaign.goals = goals
        campaign.niche = niche

        db.session.commit()
        return redirect('/sponsor_campaign')
    return render_template('edit_campaign.html', campaign=campaign)


#SPONSOR DELETE CAMPAIGN ROUTE
@app.route('/delete_campaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    return redirect('/sponsor_campaign')

#SPONSOR VIEW CAMPAIGNS ROUTE
@app.route('/view_campaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    adrequests = db.session.query(Adrequests).join(Influencer).filter(
        Adrequests.campaign_id == campaign.id,
        Adrequests.sent_by_sponsor == True,
        Influencer.flagged == 0
    ).all()
    progress = calculate_campaign_progress(campaign.start_date, campaign.end_date)
    return render_template('view_campaign.html', campaign=campaign, adrequests=adrequests, progress=progress)


#SPONSOR CAMPAIGN ROUTE
@app.route('/sponsor_campaign')
@login_required
def sponsor_campaign():
    this_id = current_user.id
    sponsor = Sponsor.query.filter_by(sponsor_id=this_id).first()
    campaigns = Campaign.query.filter_by(sponsor_id = current_user.id, flagged=0).all()
    return render_template('sponsor_campaign.html', campaigns=campaigns, sponsor=sponsor, calculate_campaign_progress=calculate_campaign_progress)
