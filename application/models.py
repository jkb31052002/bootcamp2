from flask_login import UserMixin
from .database import db
from datetime import datetime as dt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    user_role = db.Column(db.String(10), nullable=False)
    admin = db.relationship('Admin', backref='user')
    sponsor = db.relationship('Sponsor', backref='user')
    influencer = db.relationship('Influencer', backref='user')

    def get_id(self):
        return str(self.id)


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Sponsor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    company_budget = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(150), nullable=False)
    flagged = db.Column(db.Integer, default=0)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaigns = db.relationship('Campaign', backref='sponsor')

class Influencer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    niche = db.Column(db.String(150), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    flagged = db.Column(db.Integer, default=0) 
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    adrequests = db.relationship('Adrequests', backref='influencer')

class Campaign(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    campaign_budget = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    visibility = db.Column(db.String(50), nullable=False)
    goals = db.Column(db.Text, nullable=False)
    niche = db.Column(db.String(150), nullable=False)
    flagged = db.Column(db.Integer, default=0)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    adrequests = db.relationship('Adrequests', backref='campaign')

class Adrequests(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    payment_amt = db.Column(db.Integer, nullable=False)
    sent_by_sponsor = db.Column(db.Boolean, nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)



