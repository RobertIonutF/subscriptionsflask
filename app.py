from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriptions.db'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

google_bp = make_google_blueprint(scope=['profile', 'email'])
app.register_blueprint(google_bp, url_prefix='/login')
google_bp.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False

    google_info = resp.json()
    google_user_id = google_info["id"]

    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=google_user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=google_user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.", category="success")
    else:
        user = User(email=google_info["email"])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google.", category="success")

    return False

@app.route('/')
@login_required
def index():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', subscriptions=subscriptions)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_subscription():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        renewal_date = datetime.strptime(request.form['renewal_date'], '%Y-%m-%d').date()
        
        new_subscription = Subscription(name=name, price=price, renewal_date=renewal_date, user_id=current_user.id)
        db.session.add(new_subscription)
        db.session.commit()
        
        flash('Subscription added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
