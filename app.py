from flask import Flask, redirect, render_template, request, session, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Secret key for session management
db = SQLAlchemy(app)


# Define the Subscriber model
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


# Create all tables in the database within the application context
with app.app_context():
    db.create_all()


def send_email(recipient_email, message_text):
    sender_email = "crogreens1@gmail.com"
    receiver_email = "crogreens1@gmail.com"
    app_password = "bvqu pewm uryj fsgh"

    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = "New Join"

    body = message_text + '\n\n' + recipient_email
    email_message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    text = email_message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


@app.route('/send_email', methods=['POST'])
def send_email_route():
    if request.method == 'POST':
        recipient_email = request.form['recipient_email']
        message_text = request.form['message']

        # Check if email already exists in the database
        existing_subscriber = Subscriber.query.filter_by(email=recipient_email).first()
        if existing_subscriber:
            session['already_joined'] = True
            return redirect('/confirmation')

        # If email doesn't exist, add it to the database
        new_subscriber = Subscriber(email=recipient_email)
        try:
            db.session.add(new_subscriber)
            db.session.commit()
            send_email(recipient_email, message_text)
            session['success'] = True
            return redirect('/confirmation')
        except IntegrityError:
            db.session.rollback()
            session['error'] = True
            return redirect('/confirmation')


@app.route('/confirmation')
def confirmation():
    success = session.pop('success', False)
    already_joined = session.pop('already_joined', False)
    error = session.pop('error', False)
    return render_template('home.html', success=success, already_joined=already_joined, error=error)


@app.route('/post/1')
def post():
    return render_template('post1.html')


@app.route('/product/microgreens/1')
def product():
    return render_template('product1.html')


@app.route('/calculator')
def calculator():
    return render_template('calculator.html')



@app.route('/plan')
def about():
    return render_template('plan.html')



@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/microgreens')
def microgreens():
    return render_template('microgreens.html')


@app.route('/spices')
def spices():
    return render_template('spices.html')


@app.route('/veggies')
def veggies():
    return render_template('veggies.html')


@app.route('/meat')
def meat():
    return render_template('meat.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

