from flask import *
from werkzeug.utils import secure_filename
import mysql.connector
db = mysql.connector.connect(host='localhost',user='root',port=3306,database='parkingreservation')
cur = db.cursor()
import pandas as pd
from flask_mail import *

app = Flask(__name__)
app.secret_key="fcb384r23823872380237r89irw78eduwsf78we4y"


# home page
@app.route("/")
def index():
    return render_template("index.html")




# admin login page
@app.route("/admin",methods=["POST","GET"])
def admin():
    if request.method=='POST':
        form = request.form
        adminname =  form['adminname']
        password = form['adminpassword']
        if adminname =='admin' and password == 'admin':
            return render_template('adminhome.html',admin=adminname)
        else:
            return render_template('admin.html',msg="invalid Credentials")

    return render_template("admin.html")


# adding parking Details
@app.route("/addparking",methods=["POST","GET"])
def addparking():
    if request.method=="POST":
        form = request.form
        form1= request.files
        parkingslot = form['parkingslot']
        Cost = form['Cost']
        address = request.form['address']
        nameofimage = form1['nameofimage']
        # imagename = nameofimage.filename
        nameofimage.save(f'static/projectimages/{secure_filename(nameofimage.filename)}')
        sql="insert into parkingslots(parkingslot,Cost,Address,Imagename)values('%s','%s','%s','%s')"%(parkingslot,Cost,address,nameofimage.filename)
        cur.execute(sql)
        db.commit()
    return render_template("addparking.html")

# customer login
@app.route("/customer",methods=["POST","GET"])
def customer():
    if request.method=="POST":
        form = request.form
        customeremail = form['customeremail']
        customerpassword = form['customerpassword']
        sql="select * from customerreg where customeremail='%s' and customerpassword='%s'"%(customeremail,customerpassword)
        cur.execute(sql)
        dc = cur.fetchall()
        if dc !=[]:
            session['useremail']=customeremail
            return render_template("customerhome.html")
        else:
            return render_template("customer.html",msg="invalid Credentials")


    return render_template("customer.html")


# customerreg
@app.route("/customerreg",methods=["POST","GET"])
def customerreg():
    if request.method=="POST":
        form = request.form
        customername = form['customername']
        customeremail = form['customeremail']
        customerpassword = form['customerpassword']
        confirmpassword = form['confirmpassword']
        customercontact = form['customercontact']
        customeraddress = form['customeraddress']
        if customerpassword == confirmpassword:
            sql="select * from customerreg where customeremail='%s' and customerpassword='%s'"%(customeremail,customerpassword)
            cur.execute(sql)
            d = cur.fetchall()
            if d ==[]:
                sql="insert into customerreg(customername,customeremail,customerpassword,customercontact,customeraddress)values(%s,%s,%s,%s,%s)"
                val=(customername,customeremail,customerpassword,customercontact,customeraddress)
                cur.execute(sql,val)
                db.commit()
                return render_template("customer.html")
            else:
                return render_template("customerreg.html",msg="Password not matched")
        else:
            return render_template("customerreg.html",msg="Password not matched")

    return render_template("customerreg.html")


# Parking details for user

@app.route('/view_parking')
def view_parking():
    sql="select * from parkingslots"
    data = pd.read_sql_query(sql,db)
    return render_template("viewparking.html",cols=data.columns.values,rows=data.values.tolist())


@app.route("/reserveslot/<c>")
def reserveslot(c=0):
    session['c'] = c
    sql = "select * from parkingslots where id='%s'"%(c)
    cur.execute(sql)
    dc = cur.fetchall()[0]
    return render_template("reserveslot.html",dc=dc)

@app.route("/bookslot",methods=["POST","GET"])
def bookslot():
    c =session['c']
    sql = "select * from parkingslots where id='%s'"%(c)
    cur.execute(sql)
    dc = cur.fetchall()[0]
    if request.method=="POST":
        c = session['c']
        slotid = request.form['slotid']
        hourcost = request.form['hourcost']
        nameoncard = request.form['nameoncard']
        cvv = request.form['cvv']
        expiredate = request.form['expiredate']
        totalhours = request.form['totalhours']
        totalamount = request.form['totalamount']
        status = 'locked'
        sql="select * from bookslot where useremail='%s'"%(session['useremail'])
        cur.execute(sql)
        data = cur.fetchall()
        if data ==[]:
            sql="insert into bookslot(slotid,hourcost,nameoncard,cvv,expiredate,totalhours,totalamount,status,useremail)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (slotid,hourcost,nameoncard,cvv,expiredate,totalhours,totalamount,status,session['useremail'])
            cur.execute(sql,val)
            db.commit()
            sql="update parkingslots set status='locked' where id='%s'"%(c)
            cur.execute(sql)
            db.commit()
        else:
            return render_template("viewparking.html",dc=dc,msg="that slot already booked")
    return render_template("reserveslot.html",dc=dc)


@app.route("/userbookedslots")
def userbookedslots():
    sql="select id,slotid,hourcost,nameoncard,totalhours,totalamount from bookslot where status='locked'"
    data=pd.read_sql_query(sql,db)
    return render_template("userbookedslots.html",cols=data.columns.values,rows=data.values.tolist())


@app.route("/acceptrequest/<x>")
def acceptrequest(x=0):
    # sender_address = 'sender@gmail.com'
    # sender_pass = 'password'
    # content = "Your Request Is Accepted by the Admin, You Can Login Now"
    # receiver_address = session['useremail']
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = "Online Parking Reservation System"
    # message.attach(MIMEText(content, 'plain'))
    # ss = smtplib.SMTP('smtp.gmail.com', 587)
    # ss.starttls()
    # ss.login(sender_address, sender_pass)
    # text = message.as_string()
    # ss.sendmail(sender_address, receiver_address, text)
    # ss.quit()
    sql="update bookslot set status='accepted' where id='%s'"%(x)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('userbookedslots'))

@app.route("/viewresponse")
def viewresponse():
    sql="select slotid,hourcost,totalhours,totalamount,status,useremail from bookslot where status='accepted'"
    data = pd.read_sql_query(sql,db)
    return render_template("viewresponse.html",cols=data.columns.values,rows=data.values.tolist())


@app.route("/rejectrequest/<x>")
def rejectrequest(x=0):


    sender_address = 'sender@gmail.com'
    sender_pass = 'password'
    content = "Your Request Is Rejected by the Admin because of no parking slots reservation"
    receiver_address = session['useremail']
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "Online Parking Reservation System"
    message.attach(MIMEText(content, 'plain'))
    ss = smtplib.SMTP('smtp.gmail.com', 587)
    ss.starttls()
    ss.login(sender_address, sender_pass)
    text = message.as_string()
    # ss.sendmail(sender_address, receiver_address, text)
    ss.quit()
    sql="update bookslot set status='rejected' where id='%s'"%(x)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('userbookedslots'))

if __name__ =="__main__":
    app.run(debug=True)
