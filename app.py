from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriptions.db'
db = SQLAlchemy(app)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    subscriptions = Subscription.query.all()
    return render_template('index.html', subscriptions=subscriptions)

@app.route('/add', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        renewal_date = datetime.strptime(request.form['renewal_date'], '%Y-%m-%d').date()
        
        new_subscription = Subscription(name=name, price=price, renewal_date=renewal_date)
        db.session.add(new_subscription)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
