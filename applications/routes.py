from flask import request, session, render_template, flash, redirect, url_for
from main import app
from applications.models import *
from datetime import datetime

@app.route('/')
def index():
    if session.get('user_email'):
        if session['user_role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return render_template("index.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_email' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))
    
    if session['user_role'] != 'admin':
        flash("You are not authorized to access this page.", "warning")
        return redirect(url_for('user_dashboard'))
    
    users = User.query.all()
    
    return render_template('admin_dashboard.html', users=users)

from applications.utils.stock_cache import fetch_and_cache_stocks

@app.route('/user_dashboard')
def user_dashboard():
    if session.get('user_role') != 'user':
        flash("You are logged in as an admin.", "warning")
        return redirect(url_for('admin_dashboard'))

    if 'user_email' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    stocks_data = fetch_and_cache_stocks()

    # Sort by Market Cap descending
    stocks_data = [s for s in stocks_data if s.market_cap]
    stocks_data.sort(key=lambda x: x.market_cap, reverse=True)

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 20
    total = len(stocks_data)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = stocks_data[start:end]

    for idx, stock in enumerate(paginated, start=start + 1):
        stock.serial = idx  # Add serial number

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'user_dashboard.html',
        stocks=paginated,
        current_page=page,
        total_pages=total_pages
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter email and password')
            return render_template("login.html")
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found')
            return render_template("login.html")
        
        if user.password != password:
            flash('Incorrect password')
            return render_template("login.html")
        
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.name
        session['user_role'] = user.roles[0].name
        flash('Logged in successfully')
        
        if user.roles[0].name == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_role', None)
    session.pop('user_name', None)
    return redirect("/login")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        dob_str = request.form.get('dob')  # Get date string from form
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert to date object
        role = request.form.get('role')
        
        if User.query.filter_by(email=email).first():
            flash('User already exists')
            return render_template("register.html")
        
        if not email or not password or not confirm_password or not name or not dob:
            flash('Please enter all fields')
            return render_template("register.html")
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template("register.html")
        
        role_object = Role.query.filter_by(name=role).first()
        
        user = User(email=email, password=password, name=name, dob=dob, roles=[role_object])
        db.session.add(user)
        
        db.session.commit()
        flash('User Registered successfully')
        return render_template("login.html")