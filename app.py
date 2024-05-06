from flask import Flask, redirect, render_template, request, session
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
    message = db.Column(db.Text, nullable=False)


# Create all tables in the database within the application context
with app.app_context():
    db.create_all()


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
        new_subscriber = Subscriber(email=recipient_email, message=message_text)
        try:
            db.session.add(new_subscriber)
            db.session.commit()
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


# Define a dynamic route that accepts a post_id parameter
@app.route('/post/<int:post_id>')
def post(post_id):
    template_name = f'post{post_id}.html'
    # You can add logic here to fetch the post content based on post_id
    if post_id == 1:
        post_title = "Lekcije Iz Prirode II. Dio"
        post_date = "3 days ago"
        post_content = "Some placeholder content in a paragraph."
        post_additional_info = "And some muted small print."
    elif post_id == 2:
        post_title = "Priroda i strpljivost"
        post_date = "20.04.2024"
        post_content = "Zašto je strpljivost od ključne važnosti."
        post_additional_info = "I kako se strpljivost odražava na sve što radimo."
    elif post_id == 3:
        post_title = "Priroda i strpljivost"
        post_date = "20.04.2024"
        post_content = "Zašto je strpljivost od ključne važnosti."
        post_additional_info = "I kako se strpljivost odražava na sve što radimo."
    else:
        # Handle cases for other post IDs
        # For simplicity, let's just return a default message
        return "Post not found"

    # Render the template with the dynamic post content
    return render_template(template_name, title=post_title, date=post_date, content=post_content, additional_info=post_additional_info)


# Define a dynamic route that accepts a product_id parameter
@app.route('/product/microgreens/<int:product_id>')
def product(product_id):
    # Construct the template name based on the product_id
    template_name = f'product{product_id}.html'

    # Render the template with the dynamic product content
    return render_template(template_name)


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
