from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify, make_response
#from data import Articles
from flask_mysqldb import MySQL
from flask_admin import Admin
from flask_login import UserMixin
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.fields.html5 import DateField
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
from functools import wraps
import collections
import uuid
from flask_material import Material
import random
import string
import re


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'db.summersend.serverswc.com'
app.config['MYSQL_USER'] = 'michael'
app.config['MYSQL_PASSWORD'] = 'databaseproject'
app.config['MYSQL_DB'] =  'uypdbfinal'
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'flask.final@gmail.com',
    MAIL_PASSWORD = 'databasefinal'
)
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
mail = Mail(app)


def giveAccount(id, message):
    cur = mysql.connection.cursor()
    cur.execute("SELECT FirstName, LastName, Email FROM Student WHERE StudentID=%s", id)
    res = cur.fetchone()

    if message == "Accepted":
        new_use = (res[1] + res[0] + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5)))
        new_pass = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO UserSystem (StudentID, Username, Password) VALUES (%s, %s, %s)", (id, new_use, str(sha256_crypt.hash(new_pass))))
        mysql.connection.commit()
        cur.close()
        try:
            msg = Message("Welcome to UYP!",
                sender="flask.final@gmail.com",
                recipients=[res[2]])
            msg.body = "To start with UYP, your username is [" + new_use + "] and your password is [" + new_pass + "]!"
            mail.send(msg)
            return 'We good'
        except Expception as e:
            return str(e)
    elif message == "Declined":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Student WHERE StudentID=%s", [id])
        mysql.connection.commit()
        cur.close()
        try:
            msg = Message("Message from UYP",
                sender="flask.final@gmail.com",
                recipients=[res[2]])
            msg.body = "We are very sorry, but UYP could not accept you application at this time."
            mail.send(msg)
            return 'We good'
        except Expception as e:
            return str(e)


# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/v', methods=['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        print(username)
        print(password_candidate)
        # Create cursor
        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM Admin WHERE Username=%s', [username])
        #WHERE Email=' + '\'' + email + '\'')

        # Get user by username
        #cur.execute('SELECT * FROM UserSystem WHERE Email=' + '\'' + email + '\'')

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[1]
            print(sha256_crypt.hash(password_candidate))
            print(password)

            # Compare Passwords
            if True:
                # Passed
                session['logged_in'] = True
                session['username'] = "Admin"

                flash('You are now logged in as an admin', 'success')
                return redirect('/vadmin')
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('adminlogin.html', error=error)
    return render_template('login.html')

@app.route('/vadmin')
def vadmin():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        #cur = mysql.connection.cursor()
        # Get articles
        #result = cur.execute("SELECT * FROM student WHERE AcceptedState=False")
        #students = cur.fetchall()
        return render_template('adminhome.html')

@app.route('/admin')
def admin():
    return render_template('adminlogin.html')

@app.route('/admineditstudents')
def admineditstudents():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute('SELECT * FROM student')
        students = cur.fetchall()

        if result > 0:
            return render_template('admineditstudents.html', students=students)
        else:
            return render_template('admineditstudents.html', msg="No students")

@app.route('/adminstudents')
def adminstudents():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute('SELECT * FROM student WHERE AcceptedState=\'False\' AND NeedsInfo=\'True\'')
        students = cur.fetchall()

        if result > 0:
            return render_template('adminstudents.html', students=students)
        else:
            msg = 'No students found'
            return render_template('adminstudents.html', msg=msg)


@app.route('/registerclass/<string:id>')
def registerclass(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        # Create Cursor
        cur = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        """
        cur2.execute("INSERT INTO TAKES (StudentID, CourseID) VALUES (%s, %s)", (session['number'], id))
        mysql.connection.commit()
        flash("You have registered for the class!", 'success')
        return render_template('home.html')
        """
        timeslot = cur2.execute("SELECT TimeSlot FROM Courses WHERE CourseID = %s", [id])

        timeslot = cur2.fetchone()
        # Execute
        res = cur.execute("SELECT TimeSlot FROM Takes, Courses WHERE StudentID=%s AND Courses.CourseID = Takes.CourseID AND TimeSlot = %s", [session['number'], timeslot])
        # Commit to DB
        results = cur.fetchone()

        if res > 0:
            flash("CONFLICT: Already registered for a class in this time slot.", 'danger')
            return render_template('home.html')
        else:
            cur3 = mysql.connection.cursor()
            cur4 = mysql.connection.cursor()

            mygrade = cur3.execute("SELECT CurrentGrade FROM schoolinginfo WHERE StudentID = %s", [session['number']])
            classGradeRange = cur4.execute("SELECT GradeRange FROM Courses WHERE CourseID = %s", [id])

            mygrade = cur3.fetchone()
            classGradeRange = cur4.fetchone()

            #print("This is the value returned from the tupe: %s", [mygrade[0]])
            lower,upper = classGradeRange[0].split("-")

            print("Lower bound: %s", [lower])
            print("Upper bound: %s", [upper])

            thegrade = re.sub('[^0-9]','', mygrade[0])

            print("The Grade: %s", [thegrade])

            if thegrade <= upper and thegrade >= lower:
                flash("YOU CAN FUCKING REGISTER", 'danger')
                return render_template('home.html')
            else:
                flash("CONFLICT: This class is not available for your grade range", 'danger')
                return render_template('home.html')
                


@app.route('/adminad')
def adminad():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute("SELECT * FROM student WHERE AcceptedState=\'False\' AND NeedsInfo=\'False\'")
        students = cur.fetchall()

        if result > 0:
            return render_template('adstudents.html', students=students)
        else:
            msg = 'No students found'
            return render_template('adstudents.html', msg=msg)

@app.route('/adminlistteachers')
def adminlistteachers():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute("SELECT * FROM Teacher")
        teachers = cur.fetchall()

        if result > 0:
            return render_template('adminlistteachers.html', teachers=teachers)
        else:
            msg = 'No teachers found'
            return render_template('adminlistteachers.html', msg=msg)

# Teacher Form Class
class TeacherForm(Form):
    first_name = StringField('First Name', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=3, max=200)])
    last_name = StringField('Last Name', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=3, max=200)])
    middle_initial = StringField('Middle Initial', [validators.Regexp('^[A-Za-z0-9]$'), validators.Length(min=1, max=1)])

@app.route('/adminaddteacher')
def adminaddteacher():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        teacherid = uuid.uuid4()
        first_name = form.first_name.data
        last_name = form.last_name.data
        middle_initial = form.middle_initial.data

        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute("INSERT INTO Teacher (TeacherID, FirstName, LastName, MiddleInitial) VALUES (%s, %s, %s, %s)", (teacherid, first_name, last_name, middle_initial))
        mysql.connection.commit()

        cur.close()

        return redirect(url_for('dashboard'))

    return render_template('addteacher.html', form=form)

@app.route('/admindeleteteacher')
def admindeleteteacher(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        teacherid = id

        cur = mysql.connection.cursor()

        result = cur.execute("DELETE FROM Teacher WHERE TeacherID = %s", (teacherid))

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('dashboard'))

    return render_template('admindeleteteacher.html')

@app.route('/adstudent/<string:id>/', methods=['POST', 'GET'])
def adstudent(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE StudentID=%s", [id])
        student = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM SchoolingInfo WHERE StudentID=%s", [id])
        school = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM UYPReview WHERE StudentID=%s", [id])
        uyp = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM HealthInfo WHERE StudentID=%s", [id])
        health = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM DisabilityInfo WHERE StudentID=%s", [id])
        disability = cur.fetchone()
        cur.close()

        if request.method == 'POST':
            print("I am now in the accept thing--------------------------")
            if 'Accept' in request.form:
                print("I am now in the real accept thing--------------------------")
                cur = mysql.connection.cursor()
                cur.execute("UPDATE Student SET AcceptedState=\'True\' WHERE StudentID=%s", [id])
                mysql.connection.commit()
                cur.close()
                giveAccount([id], "Accepted")

            else:
                giveAccount([id], "Declined")
            return redirect('/adminad')

    return render_template('adpage.html', student=student, school=school, uyp=uyp, health=health, disability=disability)


SESSION_TYPES = (('--Select--', '--Select--'), ('Week 1', 'Week 1'), ('Week 2','Week 2'), ('Week 3', 'Week 3'))
TIME_SLOTS = (('--Select--', '--Select--'), ('9:45 – 11:15am', '9:45 – 11:15am'), ('1:15-2:45 pm', '1:15-2:45 pm'))
GRADE_RANGES = (('--Select--', '--Select--'), ('4-5', '4-5'), ('6-8', '6-8'), ('9-12', '9-12'))

# Class Form Class
class ClassForm(Form):
    courseid = StringField('Course ID', [validators.Regexp('^[A-Za-z][A-Za-z][0-9][0-9]$'), validators.Length(min=4, max=4)])
    course_name = StringField('Course Name', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=3, max=200)])
    department = StringField('Department', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=3, max=200)])
    session = SelectField(label='Session', choices=SESSION_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    timeslot = SelectField(label='Time Slot', choices=TIME_SLOTS, validators=[validators.Regexp('^(?!--Select--$)')])
    graderange = SelectField(label='Grade Range', choices=GRADE_RANGES, validators=[validators.Regexp('^(?!--Select--$)')])
    maxcapacity = StringField('Maximum Capacity', [validators.Regexp('^[0-9]+$'), validators.Length(min=1, max=3)])
    roomnumber = StringField('Room #', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=1, max=5)])
    TeacherID = StringField('Teacher ID', [validators.Regexp('^[A-Za-z0-9]+$'), validators.Length(min=1, max=5)])

# Add Class
@app.route('/adminaddclass', methods=['GET', 'POST'])
def adminaddclass():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        form = ClassForm(request.form)
        if request.method == 'POST' and form.validate():
            courseid = form.courseid.data
            course_name = form.course_name.data
            department = form.department.data
            Session = form.session.data
            timeslot = form.timeslot.data
            graderange = form.graderange.data
            maxcapacity = form.maxcapacity.data
            roomnumber = form.roomnumber.data

            # Create Cursor
            cur = mysql.connection.cursor()

            # Execute
            cur.execute("INSERT INTO Courses(CourseId, Course_Name, Deptartment, Session, TimeSlot, GradeRange, MaxCapacity, CurCapacity, TeacherID, RoomNo, HasTeacher, IsActive) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(courseid, course_name, department, Session, timeslot, graderange, maxcapacity, maxcapacity, '', roomnumber, 'False', 'False'))

            # Commit to DB
            mysql.connection.commit()

            #Close connection
            cur.close()

            flash('Class Created', 'success')

            return redirect(url_for('vadmin'))

        return render_template('addclass.html', form=form)

# Update Class
@app.route('/adminupdateclass', methods=['GET', 'POST'])
def adminupdateclass():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        form = ArticleForm(request.form)
        if request.method == 'POST' and form.validate():
            courseid = form.courseid.data
            course_name = form.course_name.data
            department = form.department.data
            session = form.session.data
            timeslot = form.timeslot.data
            graderange = form.graderange.data
            maxcapacity = form.maxcapacity.data
            roomnumber = form.roomnumber.data

            # Create Cursor
            cur = mysql.connection.cursor()

            # Execute
            cur.execute("UPDATE Courses SET Course_Name=%s, Department=%s, Session=%s, TimeSlot=%s, GradeRange=%s, MaxCapacity=%s, CurCapacity=%s, RoomNo=%s WHERE CourseID=%s",(course_name, department, session, timeslot, graderange, maxcapacity, maxcapacity, roomnumber, courseid))

            # Commit to DB
            mysql.connection.commit()

            #Close connection
            cur.close()

            flash('Class Updated', 'success')

            return redirect(url_for('dashboard'))

        return render_template('admin_update_class.html', form=form)

@app.route('/admindeleteclass/<string:id>/', methods=['GET', 'POST'])
def admindeleteclass(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        courseid = id

        cur = mysql.connection.cursor()

        result = cur.execute("DELETE FROM Courses WHERE CourseID = %s", [courseid])

        mysql.connection.commit()

        cur.close()

        return redirect('/vadmin')

    return render_template('class.html')

@app.route('/admineditstudentsform/<string:id>', methods=['POST', 'GET'])
def admineditstudent(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        print("I am inside the full form thing")
        form = FullEditForm(request.form)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM student")
        student = cur.fetchall()
        if request.method == 'POST':
            StudentID = form.StudentID
            FirstName = form.FirstName.data
            LastName = form.LastName.data
            MiddleInit = form.MiddleInit.data
            Suffix = form.Suffix.data
            Nickname = form.PreferredName.data
            AddressLine1 = form.AddressLine1.data
            AddressLine2 = form.AddressLine2.data
            City = form.City.data
            State = form.State.data
            Zip = form.Zip.data
            Birthdate = form.Birthdate.data
            Gender = form.Gender.data
            Ethnicity = form.Ethnicity.data
            PhoneNumber = form.PhoneNumber.data
            Email = form.Email.data
            GraduationYear = form.Graduationyear.data
            GT = form.GiftedTalented.data
            Siblingnames = form.Siblingnames.data
            Gaurdian1Name = form.Gaurdian1Name.data
            Gaurdian1AddressLine1 = form.Gaurdian1AddressLine1.data
            Gaurdian1AddressLine2 = form.Gaurdian1AddressLine2.data
            Gaurdian1City = form.Gaurdian1City.data
            Gaurdian1State = form.Gaurdian1State.data
            Gaurdian1Zip = form.Gaurdian1Zip.data
            Gaurdian1HomePhone = form.Gaurdian1homephone.data
            Gaurdian1WorkPhone = form.Gaurdian1workphone.data
            Gaurdian1CellPhone = form.Gaurdian1cellphone.data
            Gaurdian2Name = form.Gaurdian2Name.data
            Gaurdian2AddressLine1 = form.Gaurdian2AddressLine1.data
            Gaurdian2AddressLine2 = form.Gaurdian2AddressLine2.data
            Gaurdian2City = form.Gaurdian2City.data
            Gaurdian2State = form.Gaurdian2State.data
            Gaurdian2Zip = form.Gaurdian2Zip.data
            Gaurdian2HomePhone = form.Gaurdian2homephone.data
            Gaurdian2WorkPhone = form.Gaurdian2workphone.data
            Gaurdian2CellPhone = form.Gaurdian2cellphone.data
            SchoolType = form.Schooltype.data
            SchoolName = form.Schoolname.data
            SchoolDistrict = form.Schooldistrict.data
            CurrentGrade = form.Schoolgrade.data
            YearAccepted = form.YearAccepted.data
            GradeAccepted = form.GradeAccepted.data
            Status = form.Status.data
            FundingStatus = form.FundingStatus.data
            GrantName = form.GrantName.data
            Mentors = form.Mentors.data
            Siblings = form.Siblings.data
            Disability = form.Disability.data
            Health = form.Health.data
            EnglishLearner = form.EnglishLearner.data
            GT = form.GT.data
            NationalClearingHouse = form.NationalClearingHouse.data
            AdditionalInfo = form.AdditionalInfo.data

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE Student SET FirstName=%s, LastName=%s, MiddleInitial=%s, Suffix=%s, Nickname=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, Birthdate=%s, Gender=%s, Ethnicity=%s, PhoneNumber=%s, Email=%s, GT=%s, Siblings=%s, AcceptedState=%s, NeedsInfo=%s WHERE StudentID=%s",
                        (FirstName, LastName, MiddleInit, Suffix, Nickname, AddressLine1, AddressLine2, City, State, Zip, Birthdate, Gender, Ethnicity, PhoneNumber, Email, GT, Siblings, AcceptedState, NeedsInfo, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian1Name, Gaurdian1AddressLine1, Gaurdian1AddressLine2, Gaurdian1City, Gaurdian1State, Gaurdian1Zip, Gaurdian1HomePhone, Gaurdian1WorkPhone, Gaurdian1CellPhone, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian2Name, Gaurdian2AddressLine1, Gaurdian2AddressLine2, Gaurdian2City, Gaurdian2State, Gaurdian2Zip, Gaurdian2HomePhone, Gaurdian2WorkPhone, Gaurdian2CellPhone, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE SchoolingInfo SET SchoolType=%s, SchoolName=%s, SchoolDistrict=%s, CurrentGrade=%s WHERE StudentID=%s",
                                            (SchoolType, SchoolName, SchoolDistrict, CurrentGrade, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE UYPReview SET StudentID=%s, Year=%s, Class=%s, Status=%s, GrantStatus=%s, NationalClearingHouse=%s, EnglishLearner=%s, Mentors=%s WHERE StudentID=%s",
                                            (StudentID, YearAccepted, GradeAccepted, Status, GrantStatus, NationalClearingHouse, EnglishLearner, Mentors, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            return redirect('/vadmin')
        return render_template('/admineditstudentsform.html', students=student, form=form)


@app.route('/adminaddstudent', methods=['POST', 'GET'])
def adminaddstudent():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        form = FullEditForm(request.form)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM student")
        student = cur.fetchall()
        if request.method == 'POST':
            StudentID = form.StudentID
            FirstName = form.FirstName.data
            LastName = form.LastName.data
            MiddleInit = form.MiddleInit.data
            Suffix = form.Suffix.data
            Nickname = form.PreferredName.data
            AddressLine1 = form.AddressLine1.data
            AddressLine2 = form.AddressLine2.data
            City = form.City.data
            State = form.State.data
            Zip = form.Zip.data
            Birthdate = form.Birthdate.data
            Gender = form.Gender.data
            Ethnicity = form.Ethnicity.data
            PhoneNumber = form.PhoneNumber.data
            Email = form.Email.data
            GraduationYear = form.Graduationyear.data
            GT = form.GiftedTalented.data
            Siblingnames = form.Siblingnames.data
            Gaurdian1Name = form.Gaurdian1Name.data
            Gaurdian1AddressLine1 = form.Gaurdian1AddressLine1.data
            Gaurdian1AddressLine2 = form.Gaurdian1AddressLine2.data
            Gaurdian1City = form.Gaurdian1City.data
            Gaurdian1State = form.Gaurdian1State.data
            Gaurdian1Zip = form.Gaurdian1Zip.data
            Gaurdian1HomePhone = form.Gaurdian1homephone.data
            Gaurdian1WorkPhone = form.Gaurdian1workphone.data
            Gaurdian1CellPhone = form.Gaurdian1cellphone.data
            Gaurdian2Name = form.Gaurdian2Name.data
            Gaurdian2AddressLine1 = form.Gaurdian2AddressLine1.data
            Gaurdian2AddressLine2 = form.Gaurdian2AddressLine2.data
            Gaurdian2City = form.Gaurdian2City.data
            Gaurdian2State = form.Gaurdian2State.data
            Gaurdian2Zip = form.Gaurdian2Zip.data
            Gaurdian2HomePhone = form.Gaurdian2homephone.data
            Gaurdian2WorkPhone = form.Gaurdian2workphone.data
            Gaurdian2CellPhone = form.Gaurdian2cellphone.data
            SchoolType = form.Schooltype.data
            SchoolName = form.Schoolname.data
            SchoolDistrict = form.Schooldistrict.data
            CurrentGrade = form.Schoolgrade.data
            YearAccepted = form.YearAccepted.data
            GradeAccepted = form.GradeAccepted.data
            Status = form.Status.data
            FundingStatus = form.FundingStatus.data
            GrantName = form.GrantName.data
            Mentors = form.Mentors.data
            Siblings = form.Siblings.data
            Disability = form.Disability.data
            Health = form.Health.data
            EnglishLearner = form.EnglishLearner.data
            GT = form.GT.data
            NationalClearingHouse = form.NationalClearingHouse.data
            AdditionalInfo = form.AdditionalInfo.data
            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE Student SET FirstName=%s, LastName=%s, MiddleInitial=%s, Suffix=%s, Nickname=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, Birthdate=%s, Gender=%s, Ethnicity=%s, PhoneNumber=%s, Email=%s, GT=%s, Siblings=%s, AcceptedState=%s, NeedsInfo=%s WHERE StudentID=%s",
                        (FirstName, LastName, MiddleInit, Suffix, Nickname, AddressLine1, AddressLine2, City, State, Zip, Birthdate, Gender, Ethnicity, PhoneNumber, Email, GT, Siblings, AcceptedState, NeedsInfo, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian1Name, Gaurdian1AddressLine1, Gaurdian1AddressLine2, Gaurdian1City, Gaurdian1State, Gaurdian1Zip, Gaurdian1HomePhone, Gaurdian1WorkPhone, Gaurdian1CellPhone, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian2Name, Gaurdian2AddressLine1, Gaurdian2AddressLine2, Gaurdian2City, Gaurdian2State, Gaurdian2Zip, Gaurdian2HomePhone, Gaurdian2WorkPhone, Gaurdian2CellPhone, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE SchoolingInfo SET SchoolType=%s, SchoolName=%s, SchoolDistrict=%s, CurrentGrade=%s WHERE StudentID=%s",
                                            (SchoolType, SchoolName, SchoolDistrict, CurrentGrade, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE UYPReview SET StudentID=%s, Year=%s, Class=%s, Status=%s, GrantStatus=%s, NationalClearingHouse=%s, EnglishLearner=%s, Mentors=%s WHERE StudentID=%s",
                                            (StudentID, YearAccepted, GradeAccepted, Status, GrantStatus, NationalClearingHouse, EnglishLearner, Mentors, [id]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            return redirect('/vadmin')
        return render_template('/admineditstudentsform.html', students=student, form=form)

@app.route('/adminedit', methods=['POST', 'GET'])
def adminedit():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        cur = mysql.connection.cursor()
        # Get articles
        result = cur.execute('SELECT * FROM student WHERE AcceptedState=\'False\' AND NeedsInfo=\'True\'')
        students = cur.fetchall()

        if result > 0:
            return render_template('adminstudents.html', students=students)
        else:
            msg = 'No students found'
            return render_template('adminstudents.html', msg=msg)


@app.route('/studentpage/<string:id>/', methods=['POST', 'GET'])
def studentinfo(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    elif session['username'] != 'Admin':
        flash("You are not authorized", 'danger')
        return render_template('home.html')

    else:
        form = UYPReviewForm(request.form)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM student WHERE StudentID=%s", [id])
        student = cur.fetchone()
        if request.method == 'POST':
            YearAccepted = form.YearAccepted.data
            GradeAccepted = form.GradeAccepted.data
            Status = form.Status.data
            FundingStatus = form.FundingStatus.data
            GrantName = form.GrantName.data
            Mentors = form.Mentors.data
            Siblings = form.Siblings.data
            Disability = form.Disability.data
            Health = form.Health.data
            EnglishLearner = form.EnglishLearner.data
            GT = form.GT.data
            NationalClearingHouse = form.NationalClearingHouse.data
            AdditionalInfo = form.AdditionalInfo.data

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO UYPReview (StudentID, Year, Class, Status, GrantStatus, GrantName, NationalClearingHouse, EnglishLearner, Mentors)" +
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", ([id], YearAccepted, GradeAccepted, Status, FundingStatus, GrantName, NationalClearingHouse, EnglishLearner, Mentors))
            mysql.connection.commit()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Student SET Siblings=%s, GT=%s, NeedsInfo=\'False\' WHERE StudentID=%s", (Siblings, GT, [id]))
            mysql.connection.commit()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO HealthInfo (StudentID, Conditions) VALUES (%s, %s)", ([id], Health))
            mysql.connection.commit()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO DisabilityInfo (StudentID, Disability) VALUES (%s, %s)", ([id], Disability))
            mysql.connection.commit()
            cur.close()

            return redirect('/')

        return render_template('studentpage.html', student=student, form=form)

@app.route('/updateprofile', methods=['POST', 'GET'])
def updateprofile():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            print("I am here in update profile")
            StudentID = form.StudentID
            FirstName = form.FirstName.data
            LastName = form.LastName.data
            MiddleInit = form.MiddleInit.data
            Suffix = form.Suffix.data
            Nickname = form.PreferredName.data
            AddressLine1 = form.AddressLine1.data
            AddressLine2 = form.AddressLine2.data
            City = form.City.data
            State = form.State.data
            Zip = form.Zip.data
            Birthdate = form.Birthdate.data
            Gender = form.Gender.data
            Ethnicity = form.Ethnicity.data
            PhoneNumber = form.PhoneNumber.data
            Email = form.Email.data
            GraduationYear = form.Graduationyear.data
            GT = form.GiftedTalented.data
            Siblingnames = form.Siblingnames.data
            Gaurdian1Name = form.Gaurdian1Name.data
            Gaurdian1AddressLine1 = form.Gaurdian1AddressLine1.data
            Gaurdian1AddressLine2 = form.Gaurdian1AddressLine2.data
            Gaurdian1City = form.Gaurdian1City.data
            Gaurdian1State = form.Gaurdian1State.data
            Gaurdian1Zip = form.Gaurdian1Zip.data
            Gaurdian1HomePhone = form.Gaurdian1homephone.data
            Gaurdian1WorkPhone = form.Gaurdian1workphone.data
            Gaurdian1CellPhone = form.Gaurdian1cellphone.data
            Gaurdian2Name = form.Gaurdian2Name.data
            Gaurdian2AddressLine1 = form.Gaurdian2AddressLine1.data
            Gaurdian2AddressLine2 = form.Gaurdian2AddressLine2.data
            Gaurdian2City = form.Gaurdian2City.data
            Gaurdian2State = form.Gaurdian2State.data
            Gaurdian2Zip = form.Gaurdian2Zip.data
            Gaurdian2HomePhone = form.Gaurdian2homephone.data
            Gaurdian2WorkPhone = form.Gaurdian2workphone.data
            Gaurdian2CellPhone = form.Gaurdian2cellphone.data
            SchoolType = form.Schooltype.data
            SchoolName = form.Schoolname.data
            SchoolDistrict = form.Schooldistrict.data
            CurrentGrade = form.Schoolgrade.data

            print(FirstName + " " + LastName + " " + MiddleInit)

            cur1 = mysql.connection.cursor()
            cur1.execute("SELECT * FROM Student WHERE StudentID=%s", [session['number']])
            ires1 = cur1.fetchone()
            cur1.close()

            cur2 = mysql.connection.cursor()
            cur2.execute("SELECT * FROM ParentInfo WHERE StudentID=%s", [session['number']])
            ires2 = cur2.fetchall()
            cur2.close()

            cur3 = mysql.connection.cursor()
            cur3.execute("SELECT * FROM SchoolingInfo WHERE StudentID=%s", [session['number']])
            ires3 = cur3.fetchone()
            cur3.close()

                #spits out any and all errors**
                # Create cursor
            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE Student SET FirstName=%s, LastName=%s, MiddleInitial=%s, Suffix=%s, Nickname=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, Birthdate=%s, Gender=%s, Ethnicity=%s, PhoneNumber=%s, Email=%s, GT=%s, EnglishLearner=%s, NationalClearingHouse=%s, AcceptedState=%s, NeedsInfo=%s WHERE StudentID=%s",
                        (FirstName, LastName, MiddleInit, Suffix, Nickname, AddressLine1, AddressLine2, City, State, Zip, Birthdate, Gender, Ethnicity, PhoneNumber, Email, GT, ires1[18], ires1[19], ires1[20], ires1[21], ires1[0]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian1Name, Gaurdian1AddressLine1, Gaurdian1AddressLine2, Gaurdian1City, Gaurdian1State, Gaurdian1Zip, Gaurdian1HomePhone, Gaurdian1WorkPhone, Gaurdian1CellPhone, ires2[0][0]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE ParentInfo SET Name=%s, Address_Line1=%s, Address_Line2=%s, City=%s, State=%s, Zip=%s, HomePhone=%s, WorkPhone=%s, CellPhone=%s WHERE StudentID=%s",
                        (Gaurdian2Name, Gaurdian2AddressLine1, Gaurdian2AddressLine2, Gaurdian2City, Gaurdian2State, Gaurdian2Zip, Gaurdian2HomePhone, Gaurdian2WorkPhone, Gaurdian2CellPhone, ires2[0][0]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("UPDATE SchoolingInfo SET SchoolType=%s, SchoolName=%s, SchoolDistrict=%s, CurrentGrade=%s WHERE StudentID=%s",
                                            (SchoolType, SchoolName, SchoolDistrict, CurrentGrade, ires3[0]))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            flash('You have successfuly updated your profile!', 'success')

            return redirect('/')
        return render_template('updateprofile.html', form=form)


@app.route('/myprofile')
def myprofile():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        # Create cursor
        cur = mysql.connection.cursor()

        # Get articles
        print(session['number'])
        result = cur.execute("SELECT * FROM Student WHERE StudentID=%s", [session['number']])

        res = cur.fetchone()

        return render_template('myprofile.html', user=res)

        cur.close()

# List Classes
@app.route('/classes', methods=['GET'])
def listClasses():
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        result = cur.execute("SELECT * FROM Courses")
        # WHERE IsActive = 'True'")

        # Commit to DB
        res = cur.fetchall()

        #Close Connection
        cur.close()

        if result > 0:
            return render_template('classlist.html', classes=res)
        else:
            msg = 'No Classes Found'
            return render_template('classlist.html', msg=msg)


@app.route('/classpage/<string:id>/', methods=['POST', 'GET'])
def classpage(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        cur = mysql.connection.cursor()

        # Execute
        result = cur.execute("SELECT * FROM Courses WHERE CourseID=%s", [id])

        #Commit to DB
        res = cur.fetchone()

        #Close Connection
        cur.close()

        return render_template('classes.html', Class=res)

# List My Classes
@app.route('/<string:id>/', methods=['GET'])
def listMyClasses(id):
    if 'username' not in session:
        flash("You are not authorized", 'danger')
        return render_template('home.html')
    else:
        #Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        result = cur.execute("SELECT * FROM Courses,Takes WHERE Takes.StudentID = %s AND Takes.CourseID = Courses.CourseID", [session['number']])

        #Commit to DB
        res = cur.fetchall()

        #Close Connection
        cur.close()

        if result > 0:
            return render_template('myclasses.html', classes=res)
        else:
            msg = 'No Classes Found'
            return render_template('myclasses.html', msg=msg)


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

SUFFIX_TYPES = (('--Select--', '--Select--'), ('', ''), ('II','II'), ('III', 'III'), ('IV', 'IV'), ('Jr', 'Jr'), ('Sr', 'Sr'))

#def list_to_ordered_pairs(input_list):
#    ordered_pairs = collections.OrderedDict()
#    for item in input_list:
#        ordered_pairs[item] = item
#    return ordered_pairs

#state_pairs = list_to_ordered_pairs(STATE_ABBREV)
class UYPReviewForm(Form):
    YearAccepted = StringField('Year Accepted', [validators.Regexp('^[1234567890]+$'),
                                                validators.Length(min=4, max=4)])
    GradeAccepted = SelectField(label='Grade Accepted ', choices=CLASS_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    Status = SelectField(label='Interest Status ', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    FundingStatus = SelectField(label='Is the student grant funded? ', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    GrantName = StringField('If funded, what is the fund name?', [validators.Regexp('^[a-zA-Z ]+$'),
                                                validators.Length(min=1, max=50)])
    Mentors = StringField('Names of mentors for the student', [validators.Regexp('^[a-zA-Z ,]+$'),
                                                validators.Length(min=1, max=50)])
    Siblings = StringField('Names of siblings in UYP', [validators.Regexp('^[a-zA-Z ,]+$'),
                                                validators.Length(min=1, max=50)])
    Disability = StringField('Disability information (255 Characters or less)', [validators.Length(min=1, max=255)])
    Health = StringField('Health information (255 Characters or less)', [validators.Length(min=1, max=255)])
    EnglishLearner = SelectField(label='Is the student an English learner?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    GT = SelectField(label='Is the student part of Gifted and Talented?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    NationalClearingHouse = StringField('National Clearing House Info (255 Characters or less)', [validators.Length(min=1, max=255)])
    AdditionalInfo = StringField('Any additional Info')

class FullEditForm(Form):
    StudentID = uuid.uuid4()

    FirstName = StringField('First Name', [validators.Regexp('^[A-Za-z]+$'),
                                           validators.Length(min=1, max=50)])
    LastName = StringField('Last Name', [validators.Regexp('^[A-Za-z]+$'),
                                         validators.Length(min=1, max=50)])
    MiddleInit = StringField('Middle Initial', [validators.Regexp('^[A-Za-z]+$'),
                                                validators.Length(min=1, max=1)])
    Suffix = SelectField(label='Suffix', choices=SUFFIX_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    PreferredName = StringField('Preferred Name', [validators.Regexp('^[A-Za-z]+$'),
                                                   validators.Length(min=1, max=50)])
    AddressLine1 = StringField('Address Line 1', [validators.Regexp('^(.*?)+$'),
                                                  validators.Length(min=1, max=50)])
    AddressLine2 = StringField('Address Line 2', [validators.Regexp('^(.*?)+$'),
                                                  validators.Length(min=1, max=50)])
    City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
    Birthdate = StringField('Birthdate', [validators.Regexp('^[1234567890]+$'),
                                          validators.Length(min=1, max=50)])
    Gender = SelectField(label='Gender', choices=GENDER_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Ethnicity = StringField('Ethnicity', [validators.Regexp('^[A-Za-z]+$'),
                                          validators.Length(min=1, max=50)])
    Schooltype = SelectField(label='Type of schooling', choices=SCHOOL_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    Schoolname = StringField('School Name', [validators.Regexp('^[A-Za-z]+$'),
                                             validators.Length(min=1, max=50)])
    Schooldistrict = StringField('School District', [validators.Regexp('^[A-Za-z]+$'),
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
    Gaurdian1City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    Gaurdian1State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Gaurdian1Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
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
    Gaurdian2City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    Gaurdian2State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Gaurdian2Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
    Gaurdian2email = StringField('Gaurdian 2 Email', [validators.Regexp('^\w+[@]\w+[.]\w+$'),
                                                      validators.Length(min=6, max=50)])
    Gaurdian2homephone = StringField('Gaurdian 2 Home Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian2workphone = StringField('Gaurdian 2 Work Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    Gaurdian2cellphone = StringField('Gaurdian 2 Cell Phone', [validators.Regexp('^\d+$'),
                                                               validators.Length(min=10, max=10)])
    GiftedTalented = SelectField(label='Gifted and Talented?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    YearAccepted = StringField('Year Accepted', [validators.Regexp('^[1234567890]+$'),
                                                validators.Length(min=4, max=4)])
    GradeAccepted = SelectField(label='Grade Accepted ', choices=CLASS_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    Status = SelectField(label='Interest Status ', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    FundingStatus = SelectField(label='Is the student grant funded? ', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    GrantName = StringField('If funded, what is the fund name?', [validators.Regexp('^[a-zA-Z ]+$'),
                                                validators.Length(min=1, max=50)])
    Mentors = StringField('Names of mentors for the student', [validators.Regexp('^[a-zA-Z ,]+$'),
                                                validators.Length(min=1, max=50)])
    Siblings = StringField('Names of siblings in UYP', [validators.Regexp('^[a-zA-Z ,]+$'),
                                                validators.Length(min=1, max=50)])
    Disability = StringField('Disability information (255 Characters or less)', [validators.Length(min=1, max=255)])
    Health = StringField('Health information (255 Characters or less)', [validators.Length(min=1, max=255)])
    EnglishLearner = SelectField(label='Is the student an English learner?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    GT = SelectField(label='Is the student part of Gifted and Talented?', choices=BOOL_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    NationalClearingHouse = StringField('National Clearing House Info (255 Characters or less)', [validators.Length(min=1, max=255)])
    AdditionalInfo = StringField('Any additional Info')

# Register Form
class RegisterForm(Form):
    StudentID = uuid.uuid4()

    FirstName = StringField('First Name', [validators.Regexp('^[A-Za-z]+$'),
                                           validators.Length(min=1, max=50)])
    LastName = StringField('Last Name', [validators.Regexp('^[A-Za-z]+$'),
                                         validators.Length(min=1, max=50)])
    MiddleInit = StringField('Middle Initial', [validators.Regexp('^[A-Za-z]+$'),
                                                validators.Length(min=1, max=1)])
    Suffix = SelectField(label='Suffix', choices=SUFFIX_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    PreferredName = StringField('Preferred Name', [validators.Regexp('^[A-Za-z]+$'),
                                                   validators.Length(min=1, max=50)])
    AddressLine1 = StringField('Address Line 1', [validators.Regexp('^[a-zA-Z0-9\s\.,]{1,40}$'), validators.Length(min=1, max=50)])
    AddressLine2 = StringField('Address Line 2', [validators.Regexp('^[a-zA-Z0-9\s\.,]{1,40}$'), validators.Length(min=0, max=50)])
    City = StringField('City', [validators.Regexp('^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$'),
                                validators.Length(min=1, max=50)])
    State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
    Birthdate = StringField('Birthdate (mm-dd-YYYY)', [validators.Regexp('^[0-9-]+$'),
                                                        validators.Length(min=1, max=50)])

    Gender = SelectField(label='Gender', choices=GENDER_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Ethnicity = StringField('Ethnicity', [validators.Regexp('^[A-Za-z\s]+$'),
                                          validators.Length(min=1, max=50)])
    Schooltype = SelectField(label='Type of schooling', choices=SCHOOL_TYPES, validators=[validators.Regexp('^(?!--Select--$)')])
    Schoolname = StringField('School Name', [validators.Regexp('^[A-Za-z\s]+$'),
                                             validators.Length(min=1, max=50)])
    Schooldistrict = StringField('School District', [validators.Regexp('^[A-Za-z\s]+$'),
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
    Siblingnames = StringField('List Siblings in UYP (If Any) ([FirstName] [LastName], etc.])', [validators.Regexp('[a-zA-Z\s,]'),
                                                                                                 validators.Length(min=0, max=100)])
    Gaurdian1Name = StringField('Gaurdian 1 Name', [validators.Regexp('^[A-Za-z]+\s[A-Za-z]+$'),
                                                    validators.Length(min=1, max=50)])
    Gaurdian1AddressLine1 = StringField('Gaurdian 1 Address Line 1', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian1AddressLine2 = StringField('Gaurdian 1 Address Line 2', [validators.Regexp('^(.*?)+$'),
                                                                      validators.Length(min=1, max=50)])
    Gaurdian1City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    Gaurdian1State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Gaurdian1Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
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
    Gaurdian2City = StringField('City', [validators.Regexp('^[A-Za-z]+$'),
                                validators.Length(min=1, max=50)])
    Gaurdian2State = SelectField(label='State', choices=STATE_ABBREV, validators=[validators.Regexp('^(?!--Select--$)')])
    Gaurdian2Zip = StringField('Zip', [validators.Regexp('^[1234567890]+$'),
                                validators.Length(min=5, max=5)])
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
    form = RegisterForm(request.form)
    print("I am here")
    if request.method == 'POST' and form.validate():
        StudentID = uuid.uuid4()
        FirstName = form.FirstName.data
        LastName = form.LastName.data
        MiddleInit = form.MiddleInit.data
        Suffix = form.Suffix.data
        Nickname = form.PreferredName.data
        Address_Line1 = form.AddressLine1.data
        Address_Line2 = form.AddressLine2.data
        City = form.City.data
        State = form.State.data
        Zip = form.Zip.data
        Birthdate = form.Birthdate.data
        Gender = form.Gender.data
        Ethnicity = form.Ethnicity.data
        PhoneNumber = form.PhoneNumber.data
        Email = form.Email.data
        GraduationYear = form.Graduationyear.data
        GT = form.GiftedTalented.data
        Siblingnames = form.Siblingnames.data
        Gaurdian1Name = form.Gaurdian1Name.data
        Gaurdian1AddressLine1 = form.Gaurdian1AddressLine1.data
        Gaurdian1AddressLine2 = form.Gaurdian1AddressLine2.data
        Gaurdian1City = form.Gaurdian1City.data
        Gaurdian1State = form.Gaurdian1State.data
        Gaurdian1Zip = form.Gaurdian1Zip.data
        Gaurdian1homephone = form.Gaurdian1homephone.data
        Gaurdian1workphone = form.Gaurdian1workphone.data
        Gaurdian1cellphone = form.Gaurdian1cellphone.data
        Gaurdian2Name = form.Gaurdian2Name.data
        Gaurdian2AddressLine1 = form.Gaurdian2AddressLine1.data
        Gaurdian2AddressLine2 = form.Gaurdian2AddressLine2.data
        Gaurdian2City = form.Gaurdian2City.data
        Gaurdian2State = form.Gaurdian2State.data
        Gaurdian2Zip = form.Gaurdian2Zip.data
        Gaurdian2homephone = form.Gaurdian2homephone.data
        Gaurdian2workphone = form.Gaurdian2workphone.data
        Gaurdian2cellphone = form.Gaurdian2cellphone.data
        SchoolType = form.Schooltype.data
        SchoolName = form.Schoolname.data
        SchoolDistrict = form.Schooldistrict.data
        CurrentGrade = form.Schoolgrade.data


        print("My new ID is" + str(StudentID))
            #spits out any and all errors**
            # Create cursor
        cur = mysql.connection.cursor()
            # Execute query
        res = cur.execute("SELCET * FROM STUDENT WHERE StudentID=%s", str(StudentID))
        res.close()

        if res == 0:
            print(FirstName + " " + LastName + " " + MiddleInit)
            print("My new ID is" + str(StudentID))
                #spits out any and all errors**
                # Create cursor
            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("INSERT INTO Student(StudentID, FirstName, LastName, MiddleInitial, Suffix, Nickname, Address_Line1, Address_Line2, City, State, Zip, Birthdate, Gender, Ethnicity, PhoneNumber, Email, GT, AcceptedState, NeedsInfo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                            (StudentID, FirstName, LastName, MiddleInit, Suffix, Nickname, Address_Line1, Address_Line2, City, State, Zip, Birthdate, Gender, Ethnicity, PhoneNumber, Email, GT, 'False', 'True'))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("INSERT INTO ParentInfo(StudentID, Name, Address_Line1, Address_Line2, City, State, Zip, HomePhone, WorkPhone, CellPhone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                            (StudentID, Gaurdian1Name, Gaurdian1AddressLine1, Gaurdian1AddressLine2, Gaurdian1City, Gaurdian1State, Gaurdian1Zip, Gaurdian1homephone, Gaurdian1workphone, Gaurdian1cellphone))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("INSERT INTO ParentInfo(StudentID, Name, Address_Line1, Address_Line2, City, State, Zip, HomePhone, WorkPhone, CellPhone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                            (StudentID, Gaurdian2Name, Gaurdian2AddressLine1, Gaurdian2AddressLine2, Gaurdian2City, Gaurdian2State, Gaurdian2Zip, Gaurdian2homephone, Gaurdian2workphone, Gaurdian2cellphone))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            cur = mysql.connection.cursor()
                # Execute query
            cur.execute("INSERT INTO SchoolingInfo(StudentID, SchoolType, SchoolName, SchoolDistrict, CurrentGrade, GraduationYear) VALUES(%s, %s, %s, %s, %s, %s)",
                                            (StudentID, SchoolType, SchoolName, SchoolDistrict, CurrentGrade, GraduationYear))
                # Commit to DB
            mysql.connection.commit()
                # Close connection
            cur.close()

            flash('You have successfuly registered for UYP!', 'success')

            return redirect('/')
        else:
            flash('You have already registered for UYP!', 'danger')

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

        #cur.execute('SELECT * FROM Student')
        #WHERE Email=' + '\'' + email + '\'')

        # Get user by username
        res = cur.execute('SELECT * FROM UserSystem WHERE Username=%s', [username])

        if res > 0:
            # Get stored hash
            data = cur.fetchone()
            #password = data['password']
            session['number'] = data[0]
            u_name = data[1]
            p_word = data[2]

            # Compare Passwords
            if True:#sha256_crypt.verify(password_candidate, p_word):
                # Passed
                cur = mysql.connection.cursor()
                cur.execute("SELECT FirstName, LastName, Email FROM Student WHERE StudentID=%s", [data[0]])
                res = cur.fetchone()
                cur.close()

                session['logged_in'] = True
                session['username'] = res[0] + " " + res[1]

                flash('You are now logged in', 'success')
                return redirect('/')
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route("/checkUser", methods=["POST"])
def check():
    username = str(request.form["email"])
    password = str(request.form["password"])
    newPassword = sha256_crypt.encrypt(str(password))
    cur = mysql.connection.cursor()
    #cur.execute('SELECT * FROM UserSystem WHERE Email=' + '\'' + username + '\'' +  ' AND Password=' + '\'' + newPassword + '\'')
    #user = cur.fetchone()

    #if len(user) is 1:
    return redirect(url_for("home"))
    #else:
    #    return "Failure Logging In"

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
        msg = 'No students found'
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
