from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
import collections


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'db.summersend.serverswc.com'
app.config['MYSQL_USER'] = 'michael'
app.config['MYSQL_PASSWORD'] = 'databaseproject'
app.config['MYSQL_DB'] =  'dbproject'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


def reformat_phone(form, field):
    field.data = field.data.replace('-', '')
    return True


STATE_ABBREV = [('--Select--', '--Select--'), ('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('Arizona', 'Arizona'), ('Arkansas', 'Arkansas'), ('California', 'California'), ('Colorado', 'Colorado'),
                ('Connecticut', 'Connecticut'), ('Delaware', 'Delaware'), ('Florida', 'Florida'), ('Georgia', 'Georgia'), ('Hawaii', 'Hawaii'), ('Idaho', 'Idaho'),
                ('Illinois', 'Illinois'), ('Indiana', 'Indiana'), ('Iowa', 'Iowa'), ('Kansas', 'Kansas'), ('Kentucky', 'Kentucky'), ('Louisiana', 'Louisiana'),
                ('Maine', 'Maine'), ('Maryland', 'Maryland'), ('Massachusetts', 'Massachusetts'), ('Michigan', 'Michigan'), ('Minnesota', 'Minnesota'),
                ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'), ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'),
                 ('New Hampshire', 'New Hampshire'), ('New Jersey', 'New Jersey'),('New Mexico', 'New Mexico'), ('New York', 'New York'),
                 ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'), ('Ohio', 'Ohio'), ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'),
                 ('Pennsylvania', 'Pennsylvania'), ('Rhode Island', 'Rhode Island'), ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'),
                 ('Tennessee', 'Tennessee'), ('Texas', 'Texas'), ('Utah', 'Utah'), ('Vermont', 'Vermont'), ('Virginia', 'Virginia'), ('Washington', 'Washington'),
                 ('West Virginia', 'West Virginia'), ('Wisconsin', 'Wisconsin'), ('Wyoming', 'Wyoming')]

GENDER_ABBREV = (('--Select--', '--Select--'), ('Male', 'Male'), ('Female', 'Female'), ('Prefer not to answer', 'Prefer not to answer'))

BOOL_ABBREV = ( ('--Select--', '--Select--'), ('Yes', 'Yes'), ('No', 'No'), ('I\'m not sure', 'I\'m not sure'))

SCHOOL_TYPES = (('--Select--', '--Select--'), ('Public', 'Public'), ('Private', 'Private'), ('Home', 'Home'))

CLASS_TYPES = (('--Select--', '--Select--'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'),
                ('9th', '9th'), ('10th', '10th'), ('11th', '11th'), ('12th', '12th'))

SUFFIX_TYPES = (('--Select--', '--Select--'), ('II','II'), ('III', 'III'), ('IV', 'IV'), ('Jr', 'Jr'), ('Sr', 'Sr'))

#def list_to_ordered_pairs(input_list):
#    ordered_pairs = collections.OrderedDict()
#    for item in input_list:
#        ordered_pairs[item] = item
#    return ordered_pairs

#state_pairs = list_to_ordered_pairs(STATE_ABBREV)

# Register Form
class RegisterForm(Form):
    FirstName = StringField('First Name', [validators.Regexp('^[A-Za-z]+$'),
                                           validators.Length(min=1, max=50)])
    LastName = StringField('Last Name', [validators.Regexp('^[A-Za-z]+$'),
                                         validators.Length(min=1, max=50)])
    MiddleInit = StringField('Middle Initial', [validators.Regexp('^[A-Za-z]+$'),
                                                validators.Length(min=1, max=1)])
    Suffix = SelectField(label='Suffix', choices=SUFFIX_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    PreferredName = StringField('Preferred Name', [validators.Regexp('^[A-Za-z]+$'),
                                                   validators.Length(min=1, max=50)])
    AddressLine1 = StringField('Address Line 1', [validators.Regexp('^\w+$'),
                                                  validators.Length(min=1, max=50)])
    AddressLine2 = StringField('Address Line 2', [validators.Regexp('^\w+$'),
                                                  validators.Length(min=1, max=50)])
    City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
    Birthdate = StringField('Brithdate', [validators.Regexp('^[1234567890]+$'),
                                          validators.Length(min=1, max=50)])
    Gender = SelectField(label='Gender', choices=GENDER_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Ethnicity = StringField('Ethnicity', [validators.Regexp('^[A-Za-z]+$'),
                                          validators.Length(min=1, max=50)])
    Schooltype = SelectField(label='Type of schooling', choices=SCHOOL_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    Schoolname = StringField('School Name', [validators.Regexp('^[A-Za-z]+$'),
                                             validators.Length(min=1, max=50)])
    Schoolgrade = SelectField(label='Upcoming Grade', choices=CLASS_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])

    #TODO: Fix this
    Graduationyear = StringField('Graduation Year', [validators.Regexp('^[1234567890]+$'),
                                                     validators.Length(min=4, max=4)])
    Expectedhighschool = StringField('Expected Highschool', [validators.Regexp('^[A-Za-z]+$'),
                                                             validators.Length(min=1, max=50)])
    Email = StringField('Email', [validators.Regexp('^\w+[@]\w+[.]\w+$'),
                                  validators.Length(min=6, max=50)])
    PhoneNumber = StringField('Phone Number', [validators.Regexp('^\d+$'),
                                               validators.Length(min=10, max=10)])
    Siblingnames = StringField('List Siblings in UYP (If Any) ([FirstName] [LastName], etc.])', [validators.Regexp('(^[A-Za-z]+\s[A-Za-z]+[,]\s){0,20}$'),
                                                                                                 validators.Length(min=1, max=100)])
    Gaurdian1Name = StringField('Gaurdian 1 Name', [validators.Regexp('^[A-Za-z]+\s[A-Za-z]+$'),
                                                    validators.Length(min=1, max=50)])
    Gaurdian1AddressLine1 = StringField('Gaurdian 1 Address Line 1', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian1AddressLine2 = StringField('Gaurdian 1 Address Line 2', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian1email = StringField('Gaurdian 1 Email', [validators.Regexp('^\w+[@]\w+[.]\w+$'),
                                                      validators.Length(min=6, max=50)])
    Gaurdian1homephone = StringField('Gaurdian 1 Home Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian1workphone = StringField('Gaurdian 1 Work Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian1cellphone = StringField('Gaurdian 1 Cell Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian2Name = StringField('Gaurdian 2 Name', [validators.Regexp('^[A-Za-z]+\s[A-Za-z]+$'),
                                                    validators.Length(min=1, max=50)])
    Gaurdian2AddressLine1 = StringField('Gaurdian 2 Address Line 1', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian2AddressLine2 = StringField('Gaurdian 2 Address Line 2', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian2email = StringField('Gaurdian 2 Email', [validators.Regexp('^\w+[@]\w+[.]\w+$'),
                                                      validators.Length(min=6, max=50)])
    Gaurdian2homephone = StringField('Gaurdian 2 Home Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian2workphone = StringField('Gaurdian 2 Work Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian2cellphone = StringField('Gaurdian 2 Cell Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    GiftedTalented = SelectField(label='Gifted and Talented?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])




# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    print("I am here")
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        FirstName = form.FirstName.data
        LastName = form.LastName.data
        MiddleInit = form.MiddleInit.data
        print(FirstName + " " + LastName + " " + MiddleInit)
        # Create cursor
        #cur = mysql.connection.cursor()

        # Execute query
        #cur.execute("INSERT INTO Student(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        #mysql.connection.commit()

        # Close connection
        #cur.close()

        flash('You have successfuly registered for UYP!', 'success')

        return redirect('/')
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
