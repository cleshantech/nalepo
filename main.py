from flask import Flask,render_template,request,redirect,url_for,session,flash

from database import fetch_blogs,fetch_campaigns,fetch_contact,fetch_donation,fetch_eventreg,fetch_events,fetch_payments,fetch_users,fetch_volunteers,insert_volunteers,insert_blogs,insert_campaigns,insert_contact,insert_donations,insert_event_registration,insert_events,insert_payments,insert_users,check_user

from flask_bcrypt import Bcrypt

from functools import wraps

app = Flask(__name__)
app.secret_key = 'kkjghj'

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def users():
    users = fetch_users()
    return render_template('members.html',users = users)

@app.route('/add_users', methods = ['GET','POST'])
def add_users():
    if request.method == 'POST':
        # user_id = request.form['uid']
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = (name,email,hashed_password)
        insert_users(new_user)
        return redirect(url_for('users'))
    return render_template('members.html')


@app.route('/campaigns')
def campaigns():
    campaigns = fetch_campaigns()
    return render_template('campaigns.html',campaigns = campaigns)

@app.route('/add_campaigns', methods = ['GET','POST'])
def add_campaigns():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        goal_amount = request.form['goal']
        start_date = request.form['start']
        end_date = request.form['end']
        new_campaign = (title,description,goal_amount,start_date,end_date)
        insert_campaigns(new_campaign)
        flash("Campaign added Successfully","success")
        return redirect(url_for('campaigns'))




@app.route('/donations')
def donations():
    donations = fetch_donation()
    return render_template('donations.html',donations = donations)

@app.route('/new_donation', methods = ['GET','POST'])
def new_donations():
    if request.method == 'POST':
        user_id = request.form['uid']
        campaign_id = request.form['cid']
        amount = request.form['amount']
        news_donation = (user_id,campaign_id,amount)
        insert_donations(news_donation)
        flash("Donation Submitted Succesfully","success")
        return redirect(url_for('donations'))


@app.route('/payments')
def payments():
    payments = fetch_payments()
    donations = fetch_donation()
    return render_template('payments.html',payments = payments, donations = donations)

@app.route('/make_payments', methods = ['GET','POST'])
def make_payments():
    if request.method == 'POST':
        donation_id = request.form['did']
        provider = request.form['pname']
        amount = request.form['amount']
        new_payments = (donation_id,provider,amount)
        insert_payments(new_payments)
        flash("Payment made successfully","success")
        return redirect(url_for('payments'))

@app.route('/volunteers')
def volunteers():
    volunteers = fetch_volunteers()
    users = fetch_users()
    return render_template('volunteers.html',volunteers = volunteers, users = users)

@app.route('/add_volunteer', methods = ['GET','POST'])
def add_volunteer():
    if request.method == 'POST':
        user_id = request.form['uid']
        skills = request.form['skills']
        availability = request.form['avail']
        new_volunteer = (user_id,skills,availability)
        insert_volunteers(new_volunteer)
        flash("Volunteer added successfully","success")

@app.route('/events')
def events():
    events = fetch_events()
    return render_template('events.html',events = events)

@app.route('/add event', methods = ['GET','POST'])
def add_events():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        event_date = request.form['edate']
        location = request.form['location']
        new_event = (title,description,event_date,location)
        insert_blogs(new_event)
        flash("Event added successfully","success")
        return redirect(url_for('events'))

@app.route('/event_registration')
def event_registration():
    event_registration = fetch_eventreg()
    events = fetch_events()
    users = fetch_users()
    return render_template('event_registration.html',event_registration = event_registration, events = events, users = users)

@app.route('/blogs')
def blogs():
    blogs = fetch_blogs()
    return render_template('blogs.html',blogs = blogs)

@app.route('/add_blog', methods = ['GET','POST'])
def add_blog():
    if request.method == 'POST':
        user_id = request.form['uid']
        title = request.form['title']
        content = request.form['content']
        new_blog = (user_id,title,content)
        insert_blogs(new_blog)
        flash("Blog added successfully","success")
        return redirect(url_for('blogs')) 

@app.route('/contact')
def contact():
    contact = fetch_contact
    return render_template('contact.html',contact = contact)

@app.route('/give_feedback')
def give_feedback():
    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_feedback = (name,email,message)
        insert_contact(new_feedback)
        flash("Feedback submitted successfully","success")
        return redirect(url_for('contact'))
    
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        role = request.form['role']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = check_user(email)

        if not user:
            new_user = (name,email,hashed_password,role)
            insert_users(new_user)
            flash("User registered successfully, Login!","success")
            return redirect(url_for('login'))
        else:
            flash("User already exists, Login","error")
            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = check_user(email)

        if not user:
            flash("Please register first","error")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[3],password):
                session['email'] = email
                flash("Logged in successfully","success")
                return redirect(url_for('home'))
            else:
                flash("Wrong password. Try again","error")
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    flash("Logged out successfully","info")
    return redirect(url_for('login'))

app.run(debug=True)


    






    
