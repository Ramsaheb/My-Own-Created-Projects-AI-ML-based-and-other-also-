



# from datetime import datetime
# from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, session
# from flask_wtf import CSRFProtect
# from forms import LoginForm, RegistrationForm, MaintenanceForm, QueryForm, DailyMaintenanceForm, MonthlyMaintenanceForm
# from flask_pymongo import PyMongo
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import os

# # Initialize the app
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)

# # MongoDB configuration
# app.config["MONGO_URI"] = "mongodb://localhost:27017/admin_driver_db"
# mongo = PyMongo(app)

# # Initialize Bcrypt
# bcrypt = Bcrypt(app)

# # SQLAlchemy configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy and Migrate
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # CSRF protection
# csrf = CSRFProtect(app)

# maintenance_records = []
# monthly_maintenance_records = []

# # Define the MaintenanceUpdate model
# class MaintenanceUpdate(db.Model):
#     """Model for storing maintenance updates for buses."""
#     id = db.Column(db.Integer, primary_key=True)
#     bus_id = db.Column(db.String(10), nullable=False, index=True)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     tires = db.Column(db.String(100), nullable=True)
#     brakes = db.Column(db.String(100), nullable=True)
#     oil = db.Column(db.String(100), nullable=True)
#     engine = db.Column(db.String(100), nullable=True)
#     lights = db.Column(db.String(100), nullable=True)
#     engine_performance = db.Column(db.String(100), nullable=True)
#     transmission_fluid = db.Column(db.String(100), nullable=True)
#     battery_charger = db.Column(db.String(100), nullable=True)
#     brake_pads = db.Column(db.String(100), nullable=True)
#     comments = db.Column(db.Text, nullable=True)

#     def __repr__(self):
#         return f'<MaintenanceUpdate {self.bus_id} on {self.date}>'

# class DriverQuery(db.Model):
#     """Model for storing driver queries."""
#     id = db.Column(db.Integer, primary_key=True)
#     driver_id = db.Column(db.String(10), nullable=False)
#     bus_id = db.Column(db.String(10), nullable=False)
#     query_text = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     status = db.Column(db.String(20), nullable=False, default="Pending")

#     def __repr__(self):
#         return f'<DriverQuery {self.id} by driver {self.driver_id}>'

# class DailyMaintenanceRecord(db.Model):
#     """Model for daily maintenance records."""
#     id = db.Column(db.Integer, primary_key=True)
#     bus_id = db.Column(db.String(10), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     notes = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<DailyMaintenanceRecord {self.bus_id} on {self.date}>'

# class MonthlyMaintenanceRecord(db.Model):
#     """Model for monthly maintenance records."""
#     id = db.Column(db.Integer, primary_key=True)
#     bus_id = db.Column(db.String(10), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     maintenance_type = db.Column(db.String(100), nullable=False)
#     notes = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<MonthlyMaintenanceRecord {self.bus_id} on {self.date}>'


# # Accessing the user collections
# admin_users_collection = mongo.db.admin_users
# driver_users_collection = mongo.db.driver_users

# @app.route('/')
# def index():
#     return render_template('base.html')

# @app.route('/register_admin', methods=['GET', 'POST'])
# def register_admin():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         existing_user = admin_users_collection.find_one({"username": form.username.data})
#         if existing_user:
#             flash('User already exists. Please log in.', 'danger')
#             return redirect(url_for('login_admin'))
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         admin_users_collection.insert_one({
#             "username": form.username.data,
#             "email": form.email.data,
#             "password": hashed_password,
#             "role": "admin"
#         })
#         flash('Registration successful. Please log in.', 'success')
#         return redirect(url_for('login_admin'))
#     return render_template('register_admin.html', form=form)

# @app.route('/login_admin', methods=['GET', 'POST'])
# def login_admin():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = admin_users_collection.find_one({"username": form.username.data, "role": "admin"})
#         if user and bcrypt.check_password_hash(user['password'], form.password.data):
#             session['username'] = user['username']
#             session['role'] = 'admin'
#             flash('Login successful!', 'success')
#             return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login_admin.html', form=form)

# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if 'username' in session and session.get('role') == 'admin':
#         updates = MaintenanceUpdate.query.all()
#         return render_template('admin_dashboard.html', updates=updates)
#     else:
#         flash('Please log in as an admin to access this page.', 'warning')
#         return redirect(url_for('login_admin'))


# @app.route('/maintenance_team', methods=['GET', 'POST'])
# def maintenance_team():
#     form = MaintenanceForm()
#     if form.validate_on_submit():
#         update = MaintenanceUpdate(
#             bus_id=form.bus_id.data,
#             tires=form.tires.data,
#             brakes=form.brakes.data,
#             oil=form.oil.data,
#             engine=form.engine.data,
#             lights=form.lights.data,
#             engine_performance=form.engine_performance.data,
#             transmission_fluid=form.transmission_fluid.data,
#             battery_charger=form.battery_charger.data,
#             brake_pads=form.brake_pads.data,
#             comments=form.comments.data
#         )
#         db.session.add(update)
#         db.session.commit()
#         flash('Maintenance update submitted successfully!', 'success')
#         return redirect(url_for('admin_dashboard'))
#     return render_template('maintenance_team.html', form=form)

# @app.route('/maintenance/<int:update_id>')
# def get_maintenance_updates(update_id):
#     updates = MaintenanceUpdate.query.filter_by(id=update_id).all()
#     updates_data = [{
#         'date': update.date.strftime('%Y-%m-%d'),
#         'tires': update.tires,
#         'brakes': update.brakes,
#         'oil': update.oil,
#         'engine': update.engine,
#         'lights': update.lights,
#         'engine_performance': update.engine_performance,
#         'transmission_fluid': update.transmission_fluid,
#         'battery_charger': update.battery_charger,
#         'brake_pads': update.brake_pads,
#         'comments': update.comments
#     } for update in updates]
#     return jsonify(updates_data)

# @app.route('/edit_maintenance/<int:update_id>', methods=['GET', 'POST'])
# def edit_maintenance(update_id):
#     update = MaintenanceUpdate.query.get_or_404(update_id)
#     form = MaintenanceForm(obj=update)
#     if form.validate_on_submit():
#         update.tires = form.tires.data
#         update.brakes = form.brakes.data
#         update.oil = form.oil.data
#         update.engine = form.engine.data
#         update.lights = form.lights.data
#         update.engine_performance = form.engine_performance.data
#         update.transmission_fluid = form.transmission_fluid.data
#         update.battery_charger = form.battery_charger.data
#         update.brake_pads = form.brake_pads.data
#         update.comments = form.comments.data
#         db.session.commit()
#         flash('Maintenance update edited successfully!', 'success')
#         return redirect(url_for('admin_dashboard'))
#     return render_template('edit_maintenance.html', form=form)



# @app.route('/register_driver', methods=['GET', 'POST'])
# def register_driver():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         existing_user = driver_users_collection.find_one({"username": form.username.data})
#         if existing_user:
#             flash('Driver already exists. Please log in.', 'danger')
#             return redirect(url_for('login_driver'))
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         driver_users_collection.insert_one({
#             "username": form.username.data,
#             "password": hashed_password,
#             "role": "driver"
#         })
#         flash('Registration successful. Please log in.', 'success')
#         return redirect(url_for('login_driver'))
#     return render_template('register_driver.html', form=form)

# @app.route('/login_driver', methods=['GET', 'POST'])
# def login_driver():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = driver_users_collection.find_one({"username": form.username.data})
#         if user and bcrypt.check_password_hash(user['password'], form.password.data) and user.get('role') == 'driver':
#             session['username'] = user['username']
#             session['role'] = 'driver'
#             flash('Login successful!', 'success')
#             return redirect(url_for('driver_dashboard'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login_driver.html', form=form)

# @app.route('/driver/dashboard')
# def driver_dashboard():
#     if 'username' in session and session.get('role') == 'driver':
#         return render_template('driver_dashboard.html')
#     else:
#         flash('Please log in as a driver to access this page.', 'warning')
#         return redirect(url_for('login_driver'))

# @app.route('/checkup')
# def checkup():
#     return render_template('checkup.html')

# @app.route('/analysis')
# def analysis():
#     return render_template('analysis.html')

# @app.route('/daily_maintenance', methods=['GET', 'POST'])
# def daily_maintenance():
#     # form = DailyMaintenanceForm()
#     # if form.validate_on_submit():
#     #     # Create a new record
#     #     record = DailyMaintenanceRecord(
#     #         bus_id=form.bus_id.data,
#     #         date=form.date.data,
#     #         notes=form.notes.data
#     #     )
#     #     db.session.add(record)
#     #     db.session.commit()
#     #     flash('Daily maintenance record submitted successfully!', 'success')
#     #     return redirect(url_for('daily_maintenance'))

#     # # Fetch existing records from the database
#     # records = DailyMaintenanceRecord.query.all()

#     return render_template('daily_maintenance.html')



# @app.route('/monthly_maintenance', methods=['GET', 'POST'])
# def monthly_maintenance():
#     # form = MonthlyMaintenanceForm()
#     # if form.validate_on_submit():
#     #     record = MonthlyMaintenanceRecord(
#     #         bus_id=form.bus_id.data,
#     #         date=form.date.data,
#     #         maintenance_type=form.maintenance_type.data,
#     #         notes=form.notes.data
#     #     )
#     #     db.session.add(record)
#     #     db.session.commit()
#     #     flash('Monthly maintenance record submitted successfully!', 'success')
#     #     return redirect(url_for('monthly_maintenance'))

#     # records = MonthlyMaintenanceRecord.query.all()
#     return render_template('monthly_maintenance.html')

# @app.route('/yearly')
# def yearly():
#     # Your logic here
#     return render_template('yearly.html')




# @app.route('/submit_query', methods=['POST'])
# def submit_query():
#     form = QueryForm()  # Assume you have a QueryForm for handling submissions
#     if form.validate_on_submit():
#         new_query = DriverQuery(
#             driver_id=session.get('username'),
#             bus_id=form.bus_id.data,
#             query_text=form.query_text.data
#         )
#         db.session.add(new_query)
#         db.session.commit()
#         flash('Your query has been submitted successfully!', 'success')
#         return redirect(url_for('driver_dashboard'))
#     return render_template('driver_dashboard.html', form=form)



# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('You have been logged out!', 'info')
#     return redirect(url_for('login_admin'))

# if __name__ == '__main__':
#     app.run(debug=True)

















from datetime import datetime
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, session
from flask_wtf import CSRFProtect
from forms import LoginForm, RegistrationForm, MaintenanceForm, QueryForm, DailyMaintenanceForm, MonthlyMaintenanceForm
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import random

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin_driver_db"
mongo = PyMongo(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CSRF protection
csrf = CSRFProtect(app)

maintenance_records = []
monthly_maintenance_records = []



# Define the MaintenanceUpdate model
class MaintenanceUpdate(db.Model):
    """Model for storing maintenance updates for buses."""
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.String(10), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tires = db.Column(db.String(100), nullable=True)
    brakes = db.Column(db.String(100), nullable=True)
    oil = db.Column(db.String(100), nullable=True)
    engine = db.Column(db.String(100), nullable=True)
    lights = db.Column(db.String(100), nullable=True)
    engine_performance = db.Column(db.String(100), nullable=True)
    transmission_fluid = db.Column(db.String(100), nullable=True)
    battery_charger = db.Column(db.String(100), nullable=True)
    brake_pads = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<MaintenanceUpdate {self.bus_id} on {self.date}>'

class DriverQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.String(80), nullable=False)
    issue_details = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Pending")

    def __repr__(self):
        return f'<DriverQuery {self.id} by driver {self.driver_id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "bus_id": self.bus_id,
            "issue_details": self.issue_details,
            "status": self.status
        }



# Accessing the user collections
admin_users_collection = mongo.db.admin_users
driver_users_collection = mongo.db.driver_users

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = admin_users_collection.find_one({"username": form.username.data})
        if existing_user:
            flash('User already exists. Please log in.', 'danger')
            return redirect(url_for('login_admin'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin_users_collection.insert_one({
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password,
            "role": "admin"
        })
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login_admin'))
    return render_template('register_admin.html', form=form)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = admin_users_collection.find_one({"username": form.username.data, "role": "admin"})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            session['username'] = user['username']
            session['role'] = 'admin'
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_admin.html', form=form)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' in session and session.get('role') == 'admin':
        updates = MaintenanceUpdate.query.all()
        return render_template('admin_dashboard.html', updates=updates)
    else:
        flash('Please log in as an admin to access this page.', 'warning')
        return redirect(url_for('login_admin'))


@app.route('/maintenance_team', methods=['GET', 'POST'])
def maintenance_team():
    form = MaintenanceForm()
    if form.validate_on_submit():
        update = MaintenanceUpdate(
            bus_id=form.bus_id.data,
            tires=form.tires.data,
            brakes=form.brakes.data,
            oil=form.oil.data,
            engine=form.engine.data,
            lights=form.lights.data,
            engine_performance=form.engine_performance.data,
            transmission_fluid=form.transmission_fluid.data,
            battery_charger=form.battery_charger.data,
            brake_pads=form.brake_pads.data,
            comments=form.comments.data
        )
        db.session.add(update)
        db.session.commit()
        flash('Maintenance update submitted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('maintenance_team.html', form=form)

@app.route('/maintenance/<int:update_id>')
def get_maintenance_updates(update_id):
    updates = MaintenanceUpdate.query.filter_by(id=update_id).all()
    updates_data = [{
        'date': update.date.strftime('%Y-%m-%d'),
        'tires': update.tires,
        'brakes': update.brakes,
        'oil': update.oil,
        'engine': update.engine,
        'lights': update.lights,
        'engine_performance': update.engine_performance,
        'transmission_fluid': update.transmission_fluid,
        'battery_charger': update.battery_charger,
        'brake_pads': update.brake_pads,
        'comments': update.comments
    } for update in updates]
    return jsonify(updates_data)

@app.route('/edit_maintenance/<int:update_id>', methods=['GET', 'POST'])
def edit_maintenance(update_id):
    update = MaintenanceUpdate.query.get_or_404(update_id)
    form = MaintenanceForm(obj=update)
    if form.validate_on_submit():
        update.tires = form.tires.data
        update.brakes = form.brakes.data
        update.oil = form.oil.data
        update.engine = form.engine.data
        update.lights = form.lights.data
        update.engine_performance = form.engine_performance.data
        update.transmission_fluid = form.transmission_fluid.data
        update.battery_charger = form.battery_charger.data
        update.brake_pads = form.brake_pads.data
        update.comments = form.comments.data
        db.session.commit()
        flash('Maintenance update edited successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_maintenance.html', form=form)



@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = driver_users_collection.find_one({"username": form.username.data})
        if existing_user:
            flash('Driver already exists. Please log in.', 'danger')
            return redirect(url_for('login_driver'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        driver_users_collection.insert_one({
            "username": form.username.data,
            "password": hashed_password,
            "role": "driver"
        })
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login_driver'))
    return render_template('register_driver.html', form=form)

@app.route('/login_driver', methods=['GET', 'POST'])
def login_driver():
    form = LoginForm()
    if form.validate_on_submit():
        user = driver_users_collection.find_one({"username": form.username.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data) and user.get('role') == 'driver':
            session['username'] = user['username']
            session['role'] = 'driver'
            flash('Login successful!', 'success')
            return redirect(url_for('driver_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_driver.html', form=form)

@app.route('/driver/dashboard')
def driver_dashboard():
    if 'username' in session and session.get('role') == 'driver':
        return render_template('driver_dashboard.html')
    else:
        flash('Please log in as a driver to access this page.', 'warning')
        return redirect(url_for('login_driver'))

@app.route('/checkup')
def checkup():
    return render_template('checkup.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/daily_maintenance', methods=['GET', 'POST'])
def daily_maintenance():


    return render_template('daily_maintenance.html')



@app.route('/monthly_maintenance', methods=['GET', 'POST'])
def monthly_maintenance():


    return render_template('monthly_maintenance.html')

@app.route('/yearly')
def yearly():
    # Your logic here
    return render_template('yearly.html')

@app.route('/api/profile')
def profile():
    # Fetch driver data (username, etc.) from the session or database
    if 'username' in session and session.get('role') == 'driver':
        driver = driver_users_collection.find_one({"username": session['username']})
        
        if driver:
            driver_name = driver.get('username', 'Unknown Driver')  # Fetch the actual driver name
            
            # Generate random or actual driver details
            driver_id = random.randint(10000, 99999)  # You might want to use a real driver ID
            contact_number = random.randint(1000000000, 9999999999)  # Replace with actual contact if available
            
            # Example assigned buses (can be fetched from a database)
            assigned_buses = [
                {"bus_id": 1, "route": "Route A", "status": "Operational", "last_inspection": "Sept 18, 2024"},
                {"bus_id": 2, "route": "Route B", "status": "Operational", "last_inspection": "Sept 19, 2024"},
                {"bus_id": 3, "route": "Route C", "status": "Operational", "last_inspection": "Sept 20, 2024"}
            ]
            
            return jsonify({
                "name": driver_name,
                "driver_id": driver_id,
                "contact": contact_number,
                "assigned_buses": assigned_buses
            })
        else:
            return jsonify({"error": "Driver not found"}), 404
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)











