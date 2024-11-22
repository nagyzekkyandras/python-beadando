from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = "my_full_random_secret_key_123" # fontos adatok eláírásáshoz kell

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootpassword@mysql_db:3306/app_db'
db = SQLAlchemy(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # az oldal ahol a user authentikáció megtörténik

# DB modellek
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    title = db.Column(db.String(20), nullable=True)
    team = db.Column(db.String(20), nullable=True)

class WorkdayLocation(db.Model):
    __tablename__ = 'workday_locations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.Enum('Office', 'Home Office', 'Other'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime)

# for reasons: https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def root():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    regisztrációs funkció:
    - GET-es kérés ha van már session akkor átirányít a fő oldalra
    - GET-es kérés ha nincs még session akko betölt a regisztrációs weboldal
    - POST-os kérés esetén feldolgozza az adatokat és átdob a login oldalra, hiba esetán marad
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        phone = "00000000"
        title = "empty"
        team = "empty"
        
        # ha már létezik
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('register'))
        
        # jelszó hash
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # adatok feltöltése DB-be
        db.session.add(User(email=email, name=name, password=hashed_password, phone=phone, title=title, team=team))
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    login funkció:
    - GET-es kérés ha van már session akkor átirányít a fő oldalra
    - GET-es kérés ha nincs még session akko betölt a login weboldal
    - POST-os kérés esetén feldolgozza az adatokat és átdob a fő oldalra, hiba esetán marad
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first() # ha bármennyi ilyen van akkor hibás
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    fő oldal:
    - GET-es kérés ha van már session akkor választhatsz work_location-t
    - GET-es kérés ha nincs még session akkor betölt a login weboldal
    - POST-os kérés esetén feldolgozza a work_location-t aznapra
    """
    if request.method == 'POST':
        selected_location = request.form['location']

        existing_entry = WorkdayLocation.query.filter_by(user_id=current_user.id, work_date=datetime.date.today()).first()
        
        if existing_entry:
            existing_entry.location = selected_location
        else:
            db.session.add(WorkdayLocation(user_id=current_user.id, work_date=datetime.date.today(), location=selected_location))
        
        db.session.commit()
        flash("Work location updated successfully!", "success")
    
    # aktuális napi információ kinyerése
    current_location = WorkdayLocation.query.filter_by(user_id=current_user.id, work_date=datetime.date.today()).first()
    return render_template('dashboard.html', current_location=current_location)

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    """
    profil oldal:
    - GET-es kérés ha van már session akkor betölt a profil oldal
    - GET-es kérés ha nincs még session akkor betölt a login weboldal
    - POST-os kérés esetén feldolgozza a módosított profil adatot
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        team = request.form['team']
        title = request.form['title']
        phone = request.form['phone']
        password = request.form['password']
        
        # email ellenörzés
        if email != current_user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already taken by another user.", "danger")
                return redirect(url_for('profil'))
        
        # adat frissítés
        current_user.name = name
        current_user.team = team
        current_user.title = title
        current_user.email = email
        current_user.phone = phone
        if password:
            current_user.password = generate_password_hash(password, method='pbkdf2:sha256')
        
        db.session.commit()
        flash("Profil updated successfully!", "success")
        return redirect(url_for('profil'))
    
    return render_template('profil.html', user=current_user)

@app.route('/office')
@login_required
def office():    
    """
    office oldal:
    - GET-es kérés ha van már session akkor betölt az office oldal
    - GET-es kérés ha nincs még session akkor betölt a login weboldal
    """
    users_in_office = db.session.query(User.name, User.team, User.title, User.phone, User.email).join(
        WorkdayLocation, User.id == WorkdayLocation.user_id
    ).filter(
        WorkdayLocation.work_date == datetime.date.today(),
        WorkdayLocation.location == 'Office'
    ).all()
    print(str(users_in_office))
    return render_template('office.html', users_in_office=users_in_office)

@app.route('/logout')
@login_required
def logout():
    """
    - GET-es kérés ha van már session akkor törli a session adatokat
    - GET-es kérés ha nincs még session akkor betölt a login weboldal
    """
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(debug=True, host="0.0.0.0", port=5000)