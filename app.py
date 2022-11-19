#4 Python Flask Tutorial - Creating Navbar Using Bootstrap v5 in Flask App - Code Jana
from datetime import datetime
from decimal import Decimal
import re,os
from werkzeug.utils import secure_filename
import uuid as uuid

from flask import Flask, request, flash, url_for, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required,current_user
import mysql.connector
import MySQLdb.cursors

#from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g
import random
#first go to Terminal, then tape: pip install flask_sqlalchemy
# py -m pip install flask_login
#pip install flask mysqlclient
#pip install mysql
import mysql.connector

# MY db connection
local_server = True
app = Flask(__name__)
app.secret_key = 'kusumachandashwini'


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/departments'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/departments'
connection=mysql.connector.connect(host='localhost',
                                   database='departments',
                                   user='root',
                                   password=''
                                   )
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'departments'

db = SQLAlchemy(app)

UPLOAD_FOLDER='static/photos/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

login_manager=LoginManager()
login_manager.login_view="login"
login_manager.init_app(app)

cur=connection.cursor()
cur = connection.cursor(buffered=True)
@login_manager.user_loader
def load_user1(rollno):
    return students.query.get(int(rollno))


class depts(db.Model):
    deptId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class majors(db.Model):
    majorId = db.Column(db.Integer, primary_key=True)
    majorName = db.Column(db.String(100))

class students(db.Model,UserMixin ):
    #id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50),primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pin = db.Column(db.String(100))
    email = db.Column(db.String(250))
    username = db.Column(db.String(250))
    password = db.Column(db.String(250))
    photo = db.Column(db.String(250))
    majorId = db.Column(db.Integer)
    DeptId = db.Column(db.Integer)
    #majorId = db.Column(db.Integer, db.ForeignKey('majors.majorId'))
    def get_id(self,rollno):
        return (self.rollno)

class courses(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    courseId = db.Column(db.String(10),primary_key=True)
    description = db.Column(db.String(200))
    period = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    credit = db.Column(db.Float)
    max_capacity = db.Column(db.Integer)
    subjectId = db.Column(db.String(10))
   # subjectId = db.Column(db.String(10), db.ForeignKey('subject.subjectId'),nullable = False)
    roomId = db.Column(db.String(10))
    teacherId = db.Column(db.String(10))

class teacher(db.Model):
        teacherId = db.Column(db.String(10), primary_key=True)
        fullName = db.Column(db.String(100))
        addr = db.Column(db.String(100))

class subject(db.Model):
    subjectId = db.Column(db.String(10), primary_key=True)
    subject = db.Column(db.String(100))

class rooms(db.Model):
    roomId = db.Column(db.String(10), primary_key=True)
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)


class enrollement_course(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rollno = db.Column(db.Integer)
    courseId = db.Column(db.String(10))
    code = db.Column(db.Integer)
    mark = db.Column(db.Float)
    grad = db.Column(db.String(4))
    result = db.Column(db.String(100))


@app.route("/")
@app.route("/home")
def home():

    # Check if user is loggedin
    #if 'loggedin' in session:

        # User is loggedin show them the home page
        return render_template('home.html')
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))


@app.route("/about")
#@login_required
def about():
    if 'loggedin' in session:
        return render_template("about.html",username1=session['username'])
    return redirect(url_for('login'))


@app.route('/account/', methods=['POST', 'GET'])
#@login_required
def account():
        cur.execute('SELECT * FROM semester ')
        semester2 = cur.fetchall()
        semester = (request.form.get('semester'))
        rollno = request.form.get('rollno')
        cur.execute(
            'SELECT enrollement_course.courseId,description,semestre,mark,grad,result,credit FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
            (rollno, semester,))
        data2 = cur.fetchall()
        cur.execute(
            'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ',
            (rollno,))
        stud = cur.fetchone()

        if 'loggedin' in session:
            semester = (request.form.get('semester'))

            cur.execute(
                'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ',
                (rollno,))
            stud = cur.fetchone()
            print("rollno:",rollno)
            print("sem:", semester)
            cur.execute('SELECT * FROM semester ')
            semester2 = cur.fetchall()

            cur.execute(
                'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ',
                (rollno,))
            stud = cur.fetchone()

            cur.execute('SELECT enrollement_course.courseId,description,semestre,mark,grad,result,credit FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
             (rollno, semester,))
            data2 = cur.fetchall()



            if request.method == 'POST':
                rollno = request.form.get('rollno')
                semester = (request.form.get('semester'))

                cur.execute(
                    'SELECT count(*)  FROM enrollement_course  WHERE  rollno=%s and code=%s order by enrollement_course.courseId',
                    (rollno, semester,))
                nb = cur.fetchone()[0]

                cur.execute('SELECT * FROM semester ')
                semester2 = cur.fetchall()
                cur.execute(
                        'SELECT rollno,fname,lname,majors.majorName,depts.name,email,photo FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ',
                        (rollno,))
                stud = cur.fetchone()

                return render_template("profile.html/", semester2=semester2, stud=stud, data2=data2,username1=session['username'],nb=nb,photo=session['photo'])

            return render_template("profile.html/", semester2=semester2, stud=stud, data2=data2, username1=session['username'],photo=session['photo'])
        return redirect(url_for('login'))


@app.route("/favicon.ico")
def favicon():
    return "", 200
#------------------------------------------------------------

@app.route('/show_all')
def show_all():

    cur.execute(f"SELECT rollno, fname,lname,username,email,majorName,name,photo FROM students INNER JOIN depts on depts.deptId =students.deptId INNER JOIN majors on students.majorId=majors.majorId order by rollno ")
    posts=cur.fetchall()
    cur.execute(
        f"SELECT count(*) FROM students")
    item1 = cur.fetchone()[0]
    #connection.close()
    return render_template("show_all.html", posts=posts,item1=item1)




@app.route('/all_majors/')
def all_majors():

    cur.execute(
        f"SELECT * FROM majors")
    posts = cur.fetchall()
    cur.execute(
        f"SELECT count(*) FROM majors")
    item1 = cur.fetchone()[0]
    #connection.close()
    return render_template("all_majors.html", posts=posts,item1=item1)


@app.route('/all_courses/')
def all_courses():
    #rows1 = Students.query.all()
    cur.execute(f"SELECT *,teachers.fullName,subject.subject FROM `courses`INNER JOIN Teachers on courses.teacherId=teachers.teacherId INNER JOIN subject on courses.subjectId=subject.subjectId")
    posts=cur.fetchall()
    cur.execute(f"SELECT count(*) FROM courses")
    item1 = cur.fetchone()[0]

    return render_template("all_courses.html", posts=posts,item1=item1)




@app.route('/all_dept/')
def all_dept():
    cur.execute(
        f"SELECT deptId,name FROM depts")
    posts =cur.fetchall()
    cur.execute(
        f"SELECT count(*) FROM depts")
    item1 = cur.fetchone()[0]
    return render_template("all_dept.html", posts=posts, item1=item1)

#-----------------------------Adding functions--------------------------------
@app.route('/addMajor', methods=['POST', 'GET'])
def addMajor():
    if request.method == "POST":

        majorId = random.randint(1, 1000)
        majorName = request.form.get('major')

        cur.execute('SELECT * FROM majors WHERE majorName=%s',(majorName, ))
        record = cur.fetchone()
        if record:

            flash("Major Already Exists", "warning")
            return redirect('/addMajor')
        else:
           cur.execute('INSERT INTO majors (majorId,majorName) VALUES (%s,%s)',(majorId,majorName))

           connection.commit()
        flash("Major Addes", "success")
    return render_template('addMajor.html')


@app.route('/addDept', methods=['POST', 'GET'])
def addDept():
    if request.method == "POST":

        deptId = random.randint(1, 100)
        name = request.form.get('dept')

        cur.execute('SELECT * FROM depts WHERE name=%s',(name, ))
        record = cur.fetchone()
        if record:

            flash("Department Already Exist", "warning")
            return redirect('/addDept')
        else:
           cur.execute('INSERT INTO depts (deptId,name) VALUES (%s,%s)',(deptId,name))

           connection.commit()
        flash("Department Addes", "success")
    return render_template('addDept.html')


@app.route('/addCourse/', methods=['POST', 'GET'])
def addCourse():
    cur.execute(
        f"SELECT subjectId,subject FROM subject")
    sub = cur.fetchall()
    cur.execute(f"select * from teachers")
    tech = cur.fetchall()
    cur.execute(f"select * from rooms")
    room = cur.fetchall()
    if request.method == "POST":
        courseId = request.form.get('courseId')
        description = request.form.get('title')
        period = request.form.get('period')
        time = datetime.now()
        max_capacity = request.form.get('capacity')
        credit = request.form.get('credit')
        subjectId = request.form.get('subject')
        teacherId = request.form.get('tech')
        roomId = request.form.get('room')


        #query = db.session.query(courses).filter_by(courseId=courseId).first()
        cur.execute('SELECT * FROM courses WHERE courseId=%s', (courseId,))
        record = cur.fetchone()
        if record:
            flash("Course Already Exist", "warning")
            return redirect('/addCourse')

        else:
            #dep = courses(courseId=courseId,description=description,time=time,period=period,max_capacity=max_capacity,credit=credit,roomId=roomId,teacherId=teacherId,subjectId=subjectId)
            cur.execute('INSERT INTO courses (courseId,description,time,period,max_capacity,credit,teacherId,roomId,subjectId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (courseId,description,time,period,max_capacity,credit,teacherId,roomId,subjectId))

            connection.commit()

            flash("new course Addes", "success")
            return redirect('/all_courses')
    return render_template("addCourse.html",tech=tech, room=room,sub=sub)


@app.route('/register/', methods=['POST', 'GET'])
def register():
   # email2 = 'toto@gmail.com'
    cur.execute(
        f"SELECT * FROM majors")
    major = cur.fetchall()
    cur.execute(f"select * from depts")
    dept = cur.fetchall()
    if request.method == "POST":
        rollno = random.randint(1, 1000)
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        addr = request.form.get('addr')
        city = request.form.get('city')
        state = request.form.get('state')
        pin = request.form.get('pin')
        username = request.form.get('username')
        email2 ='toto@gmail.com'
        password = request.form.get('pwd1')
        password2 = request.form.get('pwd2')
        photo = request.files.get('photo')

        #Grad image name
        pic_filename=secure_filename(photo.filename)
        #set uuid
        pic_name=str(uuid.uuid1()) +"_" + pic_filename
        # save that Image
        saver = request.files.get('photo')
        #change it to a string to save to db
        photo=pic_name


        deptId = request.form.get('dept')
        majorId = request.form.get('major1')
        print("User emails:", email2)
        print("User major1:", majorId)

        #user = db.session.query(students).filter_by(username=username).first()
        cur.execute('SELECT * FROM students WHERE username=%s', (username,))
        user = cur.fetchone()
       # email = db.session.query(students).filter_by(email=email).first()

        cur.execute('SELECT * FROM students WHERE email=%s', (email,))
        email = cur.fetchone()
        if user:
            flash("username Already Exists", "warning")
            return redirect('/register/')
       
        elif password!=password2:
            flash("passord1 password2 do not match, try again...")
            return redirect('/register/')
        else:
            cur.execute('INSERT INTO students (rollno,fname,lname,addr,city,state,pin,username,email,password,photo,majorId,deptId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(rollno,fname,lname,addr,city,state,pin,username,email2,password,photo,majorId,deptId))


            connection.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

            flash("new student Addes", "success")
            return redirect('/show_all')
    return render_template("register.html/",major=major, dept=dept)


#---------------------------------------------------------------------------------------------------------------

@app.route('/update/<int:id>', methods=['POST', 'GET'])
#@login_required
def update(id):
    #my_data = Users.query.get(request.form.get('id'))
    cur.execute('SELECT *,photo FROM students WHERE rollno=%s', (id,))
    my_data = cur.fetchone()
    if request.method == "POST":
        if my_data:
            print("test Id:",my_data[0])
            rollno = request.form.get('rollno')
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            addr = request.form.get('addr')
            city = request.form.get('city')
            state = request.form.get('state')
            pin = request.form.get('pin')
            email2 = request.form.get('email2')
            username = request.form.get('username')
            password = request.form.get('pwd')
            photo = request.form.get('photo')
            deptId = request.form.get('deptId')
            majorId = request.form.get('majorId')
            photo = request.files.get('photo')

            # Grad image name
            pic_filename = secure_filename(photo.filename)
            # set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # save that Image
            saver = request.files.get('photo')
            # change it to a string to save to db
            photo = pic_name

            cur.execute("""UPDATE students SET rollno=%s, fname= %s,lname= %s,addr= %s,city= %s,state= %s,pin= %s,email= %s,username= %s,password= %s,photo= %s,deptId= %s,majorId=%s WHERE rollno=%s""",(rollno,fname,lname,addr,city,state,pin,email2,username,password,photo,deptId,majorId,id))
            # accept the changes
            connection.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            flash("record updated Successfully")
            return redirect('/show_all')
        else:
            flash("whoops!!! Problem fiiiii, look figure out")
            return redirect('/show_all')

    #rows1 = students.query.filter_by(rollno=id).first()
    return render_template('update.html', my_data=my_data)



@app.route('/updateCourse/<id>', methods=['POST', 'GET'])
#@login_required
def updateCourse(id):
    #my_data = Users.query.get(request.form.get('id'))
    cur.execute('SELECT * FROM courses WHERE courseId=%s', (id,))
    my_data = cur.fetchone()
    if request.method == "POST":
        if my_data:
            courseId = request.form.get('courseId')
            title = request.form.get('title')
            period = request.form.get('period')
            time = datetime.now()
            max_capacity = request.form.get('capacity')
            credit = request.form.get('credit')
            subjectId = request.form.get('subject')
            teacherId = request.form.get('tech')
            roomId = request.form.get('room')

            cur.execute("""UPDATE courses SET courseId=%s, description= %s,period= %s,time= %s,max_capacity= %s,credit= %s,subjectId= %s,teacherId= %s,roomId=%s WHERE courseId=%s""",(courseId,title,period,time,max_capacity,credit,subjectId,teacherId,roomId,id))
            # accept the changes
            connection.commit()

            flash("record updated Successfully")
            return redirect('/all_courses')
        else:
            flash("whoops!!! Problem fiiiii, look figure out")
            return redirect('/all_courses')

    #rows1 = students.query.filter_by(rollno=id).first()
    return render_template('updateCourse.html', my_data=my_data)



@app.route('/updateMajor/<id>', methods=['POST', 'GET'])
#@login_required
def updateMajor(id):

    cur.execute('SELECT * FROM majors WHERE majorId=%s', (id,))
    my_data = cur.fetchone()
    if request.method == "POST":
        if my_data:
            majorId = request.form.get('majorId')
            majorname = request.form.get('majorname')


            cur.execute("""UPDATE majors SET majorId=%s, majorName= %s WHERE majorId=%s""",(majorId,majorname,id))
            # accept the changes
            connection.commit()

            flash("record updated Successfully")
            return redirect('/all_majors')
        else:
            flash("whoops!!! Problem fiiiii, look figure out")
            return redirect('/all_majors')

    #rows1 = students.query.filter_by(rollno=id).first()
    return render_template('updateMajor.html', my_data=my_data)


@app.route('/updateDept/<id>', methods=['POST', 'GET'])
#@login_required
def updateDept(id):

    cur.execute('SELECT * FROM depts WHERE deptId=%s', (id,))
    my_data = cur.fetchone()
    if request.method == "POST":
        if my_data:
            deptId = request.form.get('deptId')
            name = request.form.get('name')


            cur.execute("""UPDATE depts SET deptId=%s, name= %s WHERE deptId=%s""",(deptId,name,id))
            connection.commit()

            flash("record updated Successfully")
            return redirect('/all_dept')
        else:
            flash("whoops!!! Problem fiiiii, look figure out")
            return redirect('/all_dept')

    return render_template('updateDept.html', my_data=my_data)





@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):

    #if request.method == "POST":
        cur.execute('DELETE FROM `students` WHERE rollno=%s', (id,))
        connection.commit()

        cur.execute(
            f"SELECT * FROM students")
        std = cur.fetchall()
        flash("Slot Deleted Successful", "danger")
        return render_template("show_all.html/",std=std)


@app.route('/deletec/<id>', methods=['POST', 'GET'])
def deletec(id):

        cur.execute('DELETE FROM `courses` WHERE courseId=%s', (id,))
        connection.commit()

        flash("Slot Deleted Successful", "danger")

        return redirect(url_for('all_courses'))


@app.route('/deleteMajor/<id>', methods=['POST', 'GET'])
def deleteMajor(id):

        cur.execute('DELETE FROM `majors` WHERE majorId=%s', (id,))
        connection.commit()

        flash("Major Deleted Successful", "danger")

        return redirect(url_for('all_majors'))



@app.route('/deleteDept/<id>', methods=['POST', 'GET'])
def deleteDept(id):

        cur.execute('DELETE FROM `depts` WHERE deptId=%s', (id,))
        connection.commit()

        flash("Dept Deleted Successful", "danger")

        return redirect(url_for('all_dept'))



@app.route('/deleteEnrollement/<string:id>/<string:sem>/', methods=('POST', 'GET'))
def deleteEnrollement(id,sem):

        cur.execute('DELETE FROM `enrollement_course` WHERE courseId=%s and code=%s' , (id,sem,))
        connection.commit()
        flash("class Deleted Successful", "danger")

        return redirect(url_for('show_all'))

#********************--------------------------


@app.route('/billing/', methods=('GET', 'POST'))
def billing():
    code = request.form.get('semester')
    nb_credit=0
    cur.execute(
            f"SELECT type FROM semester")
    type = cur.fetchall()
    amount=1
    if 'loggedin' in session:
        rollno = session['rollno']

        cur.execute(
            'SELECT sum(Credit) FROM enrollement_course,courses  WHERE courses.courseId=enrollement_course.courseId and  enrollement_course.rollno=%s and enrollement_course.code=%s ',
            (rollno, code,))
        nb_credit = cur.fetchone()[0]
        #int(nb_credit)=nb_credit

        cur.execute(
            'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s order by tuition_fees.tuitionId',
            (rollno, code,))
        data = cur.fetchall()

        cur.execute(
            f"SELECT * FROM tuition_fees")
        tuition = cur.fetchall()

        rollno = session['rollno']

        cur.execute('SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ', (session['rollno'],))
        stud = cur.fetchone()

        cur.execute(
            f"SELECT * FROM semester")
        sem = cur.fetchall()

        cur.execute(
            'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s order by tuition_fees.tuitionId',
            (rollno, code,))
        data = cur.fetchall()

        cur.execute('SELECT sum(amount) FROM charges where charges.rollno=%s and charges.code=%s', (rollno, code,))
        item = cur.fetchone()[0]
        cur.execute(f"SELECT type FROM semester")
        type = cur.fetchall()


        if request.method == 'POST':
                rollno=session['rollno']

                tuitionId = request.form.get('tuitionId')
                code = int(request.form.get('semester'))
               # amount = int(request.form.get('amount'))
                #amount =0
                creation_date = datetime.now()
                dueDate = datetime.now()
                date = datetime.now()
                #session['rollno']

                cur.execute('SELECT sum(Credit) FROM enrollement_course,courses  WHERE courses.courseId=enrollement_course.courseId and  enrollement_course.rollno=%s and enrollement_course.code=%s ',
                    (rollno, code,))
                nb_credit = cur.fetchone()[0]

                cur.execute(f"SELECT type FROM semester")
                type = cur.fetchall()
                var5 = 0 if nb_credit is None else nb_credit
                if var5 ==0:
                    flash('No tuition applicable right now ! Some classes have  to be registered  first!!!!!.....')
                    return render_template("home.html/", tuition=tuition, stud=stud, sem=sem, data=data, item=item,nb_credit=nb_credit)


                if (tuitionId==1001 and var5<6 and code ==5):
                    amount=amount + 6 * var5
                elif (tuitionId ==1001 and var5>6 and code ==5):
                    amount=4350
                elif (tuitionId ==1010 and var5<6 and code ==3):
                    amount=amount + 4 * var5
                elif (tuitionId==1010 and var5>6 and code==3):
                    amount = amount + 3510
                elif (tuitionId == 1011 and var5 < 6 and code == 4):
                    amount = amount + 20 * var5
                elif (tuitionId == '1011' and var5 > 6 and code == 4):
                    amount = amount + 3250
                else:
                    amount=650

                print('Amount is : ',amount)
                print('semester # is : ', code)
                print('tuitionId is : ', tuitionId)
                print('credit is : ', nb_credit)

                #cur.execute(
                #    'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s and charges.tuitionId=%s order by tuition_fees.tuitionId',
                 #   (rollno, code,tuitionId,))
               # data = cur.fetchall()

                cur.execute('SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s and charges.tuitionId=%s order by tuition_fees.tuitionId',
                   (rollno, code,tuitionId,))
                data = cur.fetchall()


                if data:
                    flash("this charge already registred. do again")
                    return render_template("home.html/", tuition=tuition, stud=stud, sem=sem, data=data, item=item,nb_credit=nb_credit)
                else:
                    cur.execute('INSERT INTO charges(rollno,tuitionId,code,creation_date,dueDate,amount) VALUES (%s,%s,%s,%s,%s,%s)',
                            (rollno, tuitionId, code, creation_date, dueDate,amount))
                    connection.commit()
                    flash("bills created successfully")
                    cur.execute(
                        'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s order by tuition_fees.tuitionId',
                        (rollno, code,))
                    data = cur.fetchall()

                    cur.execute('SELECT sum(amount) FROM charges where charges.rollno=%s and charges.code=%s',(rollno, code,))
                    item = cur.fetchone()[0]

                return render_template("billing.html/", tuition=tuition, stud=stud, sem=sem, data=data, item=item,nb_credit=nb_credit)
        return render_template("billing.html/", tuition=tuition,stud=stud,sem=sem,data=data,item=item,nb_credit=nb_credit)
    return redirect(url_for('login'))


@app.route('/show_bill/', methods=['POST', 'GET'])
#@login_required
def show_bill():
        cur.execute('SELECT * FROM semester ')
        semester2 = cur.fetchall()
        semester = (request.form.get('semester'))
        rollno = request.form.get('rollno')

        cur.execute(
            'SELECT sum(Credit) FROM enrollement_course,courses  WHERE courses.courseId=enrollement_course.courseId and  enrollement_course.rollno=%s and enrollement_course.code=%s ',
            (rollno, semester,))
        nb_credit = cur.fetchone()[0]

        cur.execute(
            'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s order by tuition_fees.tuitionId',
            (rollno, semester,))
        data = cur.fetchall()

        cur.execute(
            'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s order by rollno ',
            (rollno,))
        stud = cur.fetchone()

        cur.execute('SELECT sum(amount) FROM charges where charges.rollno=%s and charges.code=%s',
                    (rollno, semester,))
        nb = cur.fetchone()[0]

        # nb = cur.fetchone()[0]  null return None by default when result is, and to avoid this error, do this...
        nb = 0 if nb is None else nb

        if 'loggedin' in session:
            semester = (request.form.get('semester'))

            cur.execute(
                'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ',
                (rollno,))
            stud = cur.fetchone()
            print("rollno:",rollno)
            print("sem:", semester)
            cur.execute('SELECT * FROM semester ')
            semester2 = cur.fetchall()

            cur.execute(
                'SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s order by rollno ',
                (rollno,))
            stud = cur.fetchone()

            cur.execute(
                'SELECT tuition_fees.tuition_name,semester.semestre,charges.amount,charges.dueDate FROM charges,tuition_fees,semester,students  WHERE students.rollno=charges.rollno and tuition_fees.tuitionId=charges.tuitionId and semester.code=charges.code and charges.rollno=%s and semester.code=%s order by tuition_fees.tuitionId',
                (rollno, semester,))
            data = cur.fetchall()

            cur.execute(
                'SELECT sum(Credit) FROM enrollement_course,courses  WHERE courses.courseId=enrollement_course.courseId and  enrollement_course.rollno=%s and enrollement_course.code=%s ',
                (rollno, semester,))
            nb_credit = cur.fetchone()[0]

            cur.execute(
                'SELECT loanName,amountReceived,date FROM grantreceived,scholarships WHERE scholarships.PellGrantId=grantreceived.PellGrantId and grantreceived.rollno=%s and grantreceived.code=%s',
                (rollno, semester,))
            grant = cur.fetchall()

            cur.execute('SELECT sum(amountReceived) FROM grantreceived where grantreceived.rollno=%s and grantreceived.code=%s',
                        (rollno, semester,))
            total = cur.fetchone()[0]
            total = 0 if total is None else total

            if request.method == 'POST':
                rollno = request.form.get('rollno')
                semester = (request.form.get('semester'))

                cur.execute(
                    'SELECT sum(Credit) FROM enrollement_course,courses  WHERE courses.courseId=enrollement_course.courseId and  enrollement_course.rollno=%s and enrollement_course.code=%s ',
                    (rollno, semester,))
                nb_credit = cur.fetchone()[0]

                cur.execute('SELECT sum(amount) FROM charges where charges.rollno=%s and charges.code=%s',
                            (rollno, semester,))
                nb = cur.fetchone()[0]

                # nb = cur.fetchone()[0]  null return None by default when result is, and to avoid this error, do this...
                nb = 0 if nb is None else nb

                cur.execute('SELECT * FROM semester ')
                semester2 = cur.fetchall()

                cur.execute('SELECT loanName,amountReceived,date FROM grantreceived,scholarships WHERE scholarships.PellGrantId=grantreceived.PellGrantId and grantreceived.rollno=%s and grantreceived.code=%s',
                            (rollno, semester,))
                grant = cur.fetchall()

                cur.execute(
                        'SELECT rollno,fname,lname,majors.majorName,depts.name,email,photo FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s order by rollno ',
                        (rollno,))
                stud = cur.fetchone()

                return render_template("show-bill.html/", semester2=semester2, stud=stud, data=data,username1=session['username'],nb=nb,photo=session['photo'],nb_credit=nb_credit,grant=grant,total=total)

            return render_template("show-bill.html/", semester2=semester2, stud=stud, data=data, username1=session['username'],photo=session['photo'],nb_credit=nb_credit,grant=grant,nb=nb,total=total)
        return redirect(url_for('login'))




@app.route('/all_registred_course/')
def all_registred_course():
    posts = Courses.query.all()
    stud = Students.query.all()

    return render_template('all_registred_course.html', posts=posts,stud=stud)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++

#add new class
@app.route('/enrollement_course2/', methods=('GET', 'POST'))
def enrollement_course2():
    code = request.form.get('semester')
    courseId = request.form.get('course')

    cur.execute('SELECT max_capacity FROM courses  WHERE  courseId=%s', (courseId,))
    max_cap = cur.fetchone()
    max_cap = 0 if max_cap is None else max_cap

    cur.execute(
        'SELECT count(*)  FROM enrollement_course  WHERE  courseId=%s and code=%s order by enrollement_course.courseId',
        (courseId, code,))
    total = cur.fetchone()[0]
    total = 0 if total is None else total

    if 'loggedin' in session:
        rollno = session['rollno']
        cur.execute(
            'SELECT enrollement_course.courseId,description,semestre,mark,grad,result FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
            (rollno, code,))
        data = cur.fetchall()

        cur.execute(
            'SELECT count(*)  FROM enrollement_course  WHERE  rollno=%s and code=%s order by enrollement_course.courseId',
            (rollno, code,))
        nb = cur.fetchone()[0]


        cur.execute(
            f"SELECT * FROM courses")
        course = cur.fetchall()
        rollno = session['rollno']
        cur.execute('SELECT rollno,fname,lname,majors.majorName,depts.name,email FROM students,majors,depts WHERE students.majorId=majors.majorId and students.deptId=depts.deptId and  rollno=%s ', (session['rollno'],))
        stud = cur.fetchone()

        cur.execute(
            f"SELECT * FROM semester")
        sem = cur.fetchall()

        cur.execute('SELECT max_capacity FROM courses  WHERE  courseId=%s', (courseId,))
        max_cap = cur.fetchone()
        max_cap = 0 if max_cap is None else max_cap

        cur.execute(
            'SELECT enrollement_course.courseId,description,semestre,mark,grad,result FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
            (rollno, code,))
        data = cur.fetchall()


        if request.method == 'POST':
            rollno=session['rollno']

            courseId = request.form.get('course')
            code = int(request.form.get('semester'))
            mark = int(request.form.get('mark'))

            cur.execute('SELECT max_capacity FROM courses  WHERE  courseId=%s', (courseId,))
            max_cap = cur.fetchone()[0]
            max_cap = 0 if max_cap is None else max_cap

            if mark>=90:
                grad='A'
            elif mark>=80:
                grad='B'

            elif mark>=70:
                grad='C'
            elif mark>=60:
                grad='D'
            else:
                grad='F'

            if mark>=60:
                result='passed'
            else:
                result='failed'

            session['rollno']
            cur.execute(
                'SELECT count(*) as nb,enrollement_course.courseId,description,semestre,mark,grad,result FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
                (rollno, code,))
            data = cur.fetchall()

            cur.execute(
                'SELECT count(*)  FROM enrollement_course  WHERE  courseId=%s and code=%s order by enrollement_course.courseId',
                (courseId, code,))
            total = cur.fetchone()[0]
            total = 0 if total is None else total

            cur.execute(
                'SELECT count(*)  FROM enrollement_course  WHERE  rollno=%s and code=%s order by enrollement_course.courseId',
                (rollno, code,))
            nb = cur.fetchone()[0]

            cur.execute(
                'SELECT * FROM enrollement_course  WHERE  rollno=%s and code=%s and courseId=%s ',
                (rollno, code, courseId,))
            test = cur.fetchall()

            if test:
                flash("already exists!!!!!")
                return render_template("home.html/", course=course,stud=stud,sem=sem,data=data,nb=nb,max_cap=max_cap,total=total)

            cur.execute(
                'SELECT * FROM enrollement_course  WHERE  rollno=%s  and courseId=%s and enrollement_course.mark>60 ',
                (rollno, courseId,))
            test2 = cur.fetchall()
            if test2:
               flash("Sorry, You can  not retake this class again. You already passed it !!!!!")
               return render_template("home.html/", course=course,stud=stud,sem=sem,data=data,nb=nb,max_cap=max_cap,total=total)

            if total>=max_cap:
                flash("Sorry, the class is full !!!!!")
                return render_template("home.html/", course=course, stud=stud, sem=sem, data=data, nb=nb,max_cap=max_cap,total=total)

            cur.execute('INSERT INTO enrollement_course(courseId,rollno,code,mark,grad,result) VALUES (%s,%s,%s,%s,%s,%s)', (courseId, rollno,code,mark,grad,result))
            connection.commit()

            flash("Classe Added successfully")
            cur.execute(
                'SELECT enrollement_course.courseId,description,semestre,mark,grad,result FROM enrollement_course,courses,semester  WHERE courses.courseId=enrollement_course.courseId and semester.code=enrollement_course.code and rollno=%s and enrollement_course.code=%s order by courseId',
                (rollno, code,))
            data = cur.fetchall()

            cur.execute(
                'SELECT count(*)  FROM enrollement_course  WHERE  rollno=%s and code=%s order by enrollement_course.courseId',
                (rollno, code,))
            nb = cur.fetchone()[0]

            cur.execute(
                'SELECT count(*)  FROM enrollement_course  WHERE  courseId=%s and code=%s order by enrollement_course.courseId',
                (courseId, code,))
            total = cur.fetchone()[0]
            total = 0 if total is None else total
            print('total is:',total)
            print('mas is', max_cap)
            return render_template("enrollement_course.html/",course=course,stud=stud,sem=sem,data=data,username1=session['username'],nb=nb,max_cap=max_cap,total=total)
        return render_template("enrollement_course.html/", course=course,stud=stud,sem=sem,data=data,nb=nb,max_cap=max_cap,total=total)
    return redirect(url_for('login'))

@app.route('/show_by_sem/', methods=['POST', 'GET'])
#@login_required
def show_by_sem():
        cur.execute('SELECT * FROM semester ')
        semester2 = cur.fetchall()
        cur.execute('SELECT * FROM courses ')
        course2 = cur.fetchall()

        semester = (request.form.get('semester'))
        courseId = request.form.get('course')

        cur.execute(
            'SELECT enrollement_course.rollno,fname,lname,courseId,username FROM enrollement_course,students  WHERE students.rollno=enrollement_course.rollno and enrollement_course.courseId=%s and enrollement_course.code=%s order by enrollement_course.rollno ',
            (courseId, semester,))
        list = cur.fetchall()
        cur.execute(
            'SELECT count(*) FROM enrollement_course,students  WHERE students.rollno=enrollement_course.rollno and enrollement_course.courseId=%s and enrollement_course.code=%s order by enrollement_course.rollno ',
            (courseId, semester,))
        total = cur.fetchone()[0]
        cur.execute('SELECT max_capacity FROM courses  WHERE  courseId=%s', (courseId,))
        max_cap = cur.fetchone()
        max_cap = 0 if max_cap is None else max_cap
        if 'loggedin' in session:
            semester = (request.form.get('semester'))
            courseId = request.form.get('course')


            cur.execute('SELECT * FROM semester ')
            semester2 = cur.fetchall()


            if request.method == 'POST':
                rollno = request.form.get('rollno')
                semester = (request.form.get('semester'))

                cur.execute(
                    'SELECT enrollement_course.rollno,fname,lname,courseId,username FROM enrollement_course,students  WHERE students.rollno=enrollement_course.rollno and enrollement_course.courseId=%s and enrollement_course.code=%s order by enrollement_course.rollno ',
                    (courseId, semester,))
                list = cur.fetchall()

                cur.execute(
                    'SELECT count(*) FROM enrollement_course,students  WHERE students.rollno=enrollement_course.rollno and enrollement_course.courseId=%s and enrollement_course.code=%s order by enrollement_course.rollno ',
                    (courseId, semester,))
                total = cur.fetchone()[0]

                cur.execute('SELECT max_capacity FROM courses  WHERE  courseId=%s', (courseId,))
                max_cap = cur.fetchone()[0]
                max_cap = 0 if max_cap is None else max_cap
                return render_template("show_class_by_semester.html/",list=list,semester2 =semester2,course2=course2,total=total,max_cap=max_cap)

            return render_template("show_class_by_semester.html/", list=list,semester2 =semester2,course2=course2,total=total,max_cap=max_cap)
        return redirect(url_for('login'))



#------------------------------------------------------------------------------------



@app.route("/login",methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cur.execute('SELECT * FROM semester ')
    semester2 = cur.fetchall()

    cur.execute('SELECT * FROM students WHERE username=%s and password=%s', (username, password,))
    record = cur.fetchone()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        cur.execute('SELECT * FROM students WHERE username=%s and password=%s',(username,password,))
        record=cur.fetchone()

        if record:
            session['loggedin']=True

            session['rollno'] = record[0]
            session['fname'] = record[1]
            session['lname'] = record[2]
            session['addr'] = record[3]
            session['city'] = record[4]
            session['state'] = record[5]
            session['pin'] = record[6]

            session['email'] = record[7]
            session['username'] = record[8]
            session['password'] = record[9]
            session['majorId'] = record[10]
            session['DeptId'] = record[11]
            session['photo'] = record[12]

            return render_template("profile.html/",record=record,semester2=semester2,username1=session['username'])
        else:
            flash('Username or Password Incorrect', "Danger")
            return redirect(url_for('login'))

               # if the user doesn't exist or password is wrong, reload the page
    return render_template("login.html",record=record)



@app.route('/logout')
def logout():
    #logout_user()
    session.pop('loggedin', None)
    session.pop('username',None)
    session.pop('rollno', None)
    session.pop('fname', None)
    session.pop('lname', None)
    session.pop('username', None)
    session.pop('addr', None)
    session.pop('email', None)
    session.pop('majorId', None)
    session.pop('DeptId', None)
    return redirect(url_for('login'))


#*********************************************
if __name__ == '__main__':
    #db.drop_all()
    #db.metadata.create_all(engine)
    db.create_all()
    app.run(debug=True)