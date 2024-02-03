from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from emailforms.models import EmailInput
import psycopg2
import logging
from configparser import ConfigParser
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

logging.basicConfig(filename="djangoLog.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db ={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        logging.debug("Ya done messed up the SQL connection")

    return db

params = config ()
logging.debug("Connecting to Postgres")
conn = psycopg2.connect(**params)
cur = conn.cursor()
logging.debug(conn.get_dsn_parameters())

def generateUserID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))

def sendmail(job_id, msp_id):
    updateUserIDSQL = """INSERT INTO tracking(user_id,email_address,msp_id) VALUES(%s,%s,%s)"""
    sender_email = "fish@praetorianguard.io"
    sender_pw = "Blackdeck1!"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email testing"
    message["From"] = sender_email
    message['Disposition-Notification-To']=sender_email
    context = ssl.create_default_context()
    text = "This is a test email"
    emails = []
    emailQuery = """SELECT email_1,email_2,email_3,email_4,email_5,email_6,email_7,email_8,email_9,email_10,email_11,email_12,email_13,email_14,email_15,email_16,email_17,email_18,email_19,email_20,email_21,email_22,email_23,email_24,email_25,email_26,email_27,email_28,email_29,email_30 FROM emailforms_emailinput WHERE job_id=%s"""
    cur.execute(emailQuery, (job_id,))
    sqlreturns = cur.fetchone()
    for sql in sqlreturns:
        if sql != 'False':
            emails.append(sql)
    for email in emails:
        message["To"] = email
        userid = generateUserID()
        cur.execute(updateUserIDSQL, (userid,email,msp_id))
        conn.commit()
        html = f"""<html><p>This is an HTML email  <img src="http://107.195.20.91:5000/pixel.gif?uid={userid}" width="1" height="1"></p><p>Random Compelling reason to click email click <a href="http://107.195.20.91:5000/linkclicked?uid={userid}">here</a> to find out who</p></html>"""
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        #message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP_SSL("mail.privateemail.com", 465, context = context) as server:
            server.login(sender_email, sender_pw)
            server.sendmail(
                sender_email, email, message.as_string()
            )

# Create your views here.

def phishing(request):

    return render(request, 'emailforms/phishing.html')

def emailsinput(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            msp_id = request.user.username
            job_id = request.POST['job_id']
            email_1 = request.POST['email_1'] 
            email_2 = request.POST.get('email_2', False)
            email_3 = request.POST.get('email_3', False)
            email_4 = request.POST.get('email_4', False)
            email_5 = request.POST.get('email_5', False)
            email_6 = request.POST.get('email_6', False)
            email_7 = request.POST.get('email_7', False)
            email_8 = request.POST.get('email_8', False)
            email_9 = request.POST.get('email_9', False)
            email_10 = request.POST.get('email_10', False)
            email_11 = request.POST.get('email_11', False)
            email_12 = request.POST.get('email_12', False)
            email_13 = request.POST.get('email_13', False)
            email_14 = request.POST.get('email_14', False)
            email_15 = request.POST.get('email_15', False)
            email_16 = request.POST.get('email_16', False)
            email_17 = request.POST.get('email_17', False)
            email_18 = request.POST.get('email_18', False)
            email_19 = request.POST.get('email_19', False)
            email_20 = request.POST.get('email_20', False)
            email_21 = request.POST.get('email_21', False)
            email_22 = request.POST.get('email_22', False)
            email_23 = request.POST.get('email_23', False)
            email_24 = request.POST.get('email_24', False)
            email_25 = request.POST.get('email_25', False)
            email_26 = request.POST.get('email_26', False)
            email_27 = request.POST.get('email_27', False)
            email_28 = request.POST.get('email_28', False)
            email_29 = request.POST.get('email_29', False)
            email_30 = request.POST.get('email_30', False)
            #need to add templates

            job = EmailInput(job_id=job_id, email_1=email_1, email_2=email_2, email_3=email_3, email_4=email_4, email_5=email_5, email_6=email_6, email_7=email_7, 
            email_8=email_8, email_9=email_9, email_10=email_10, email_11=email_11, email_12=email_12, email_13=email_13, email_14=email_14, email_15=email_15, 
            email_16=email_16, email_17=email_17, email_18=email_18, email_19=email_19, email_20=email_20, email_21=email_21, email_22=email_22, email_23=email_23, 
            email_24=email_24, email_25=email_25, email_26=email_26, email_27=email_27, email_28=email_28, email_29=email_29, email_30=email_30 )

            job.save()

            sendmail(job_id, msp_id)

            return redirect('success')
        else:
            return redirect('home:login')
    return render(request, 'emailforms/emailsinput.html')

def success(request):
    return render(request, 'emailforms/success.html')