from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import psycopg2
import logging
from configparser import ConfigParser
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import base64
import string
from .models import Campaigns, EmailTracking
from users.models import Companies


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

def gotYou(userid):
    ### add sanitization. Require exact chars and remove anything that not alphanumeric
    updateSQL = """ UPDATE phishing_emailtracking SET (email_time, email_clicked) = (%s,%s) WHERE tracking_id = %s"""
    noCap = True
    capturedTime = datetime.now()
    cur.execute(updateSQL, (capturedTime,noCap, userid))
    conn.commit() 

def gotYouLink(userid):
    linkclickedSQL = """INSERT INTO phishing_emailtracking(tracking_id,link_time,link_clicked) VALUES(%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET (user_id,link_time,link_clicked) = (EXCLUDED.user_id,EXCLUDED.link_time,EXCLUDED.link_clicked);"""
    updateclickedSQL = """ UPDATE phishing_emailtracking SET (link_time, link_clicked) = (%s,%s) WHERE tracking_id = %s"""
    noCap = True
    capturedTime = datetime.now()
    logging.debug(userid)
    cur.execute(updateclickedSQL, (capturedTime,noCap,userid))
    conn.commit()

def generateUserID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))

def generateCampaignID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(32))

def sendmail(job_id, msp_id, company_name, campaign_name, campaign_id, template_name, primary_mail_domain, emails):
    ####Get if verified
    c = Companies.objects.get(company_name=company_name, msp_id=msp_id)
    cverified = c.is_verified
    if cverified:
        updateUserIDSQL = """INSERT INTO phishing_emailtracking(tracking_id,target_email,msp_id,company_name,campaign_name,campaign_id,template_name) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        sender_email = "fish@praetorianguard.io"
        sender_pw = "Blackdeck1!"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email testing"
        message["From"] = sender_email
        message['Disposition-Notification-To']=sender_email
        context = ssl.create_default_context()
        text = "This is a test email"
        for email in emails:
            if email != False:
                message["To"] = email
                userid = generateUserID()
                cur.execute(updateUserIDSQL, (userid,email,msp_id, company_name, campaign_name,campaign_id,template_name))
                conn.commit()
                with open("/Users/hackintosh/Github/PraetorianGuard/PraetorianGuard/templates/emailtemplates/microsoftemail.html", 'r', encoding='utf-8') as file:
                    html = file.read()
                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText(html, "html")
                    #message.attach(part1)
                    message.attach(part2)
                    with smtplib.SMTP_SSL("mail.privateemail.com", 465, context = context) as server:
                        server.login(sender_email, sender_pw)
                        server.sendmail(
                            sender_email, email, message.as_string()
                        )
    else:
        raise Http404
# Create your views here.

def tracked(request):
    whoami = request.GET.get('uid', '')
    gotYouLink(whoami)
    return render(request, 'phishing/tracked.html')


@login_required(login_url='home:login')
def emailsinput(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            msp_id = request.user.username
            date = request.POST['job_id']
            company_name = request.POST.get('company_name')
            campaign_name = request.POST['campaign_name']
            campaign_id = generateCampaignID()
            template_name = request.POST['template_name']
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

            
            ##### Need to get primary_mail_domain here from sql
            getPrimDomainSQL = """SELECT primary_mail_domain FROM users_companies WHERE company_name=%s AND msp_id=%s;"""
            cur.execute(getPrimDomainSQL,(company_name,msp_id))
            primary_mail_domain = cur.fetchone()
            #need to add templates
            emails = [email_1,email_2,email_3,email_4,email_5,email_6,email_7,email_8,email_9,email_10,email_11,email_12,email_13,email_14,email_15,email_16,email_17,email_18,email_19,email_20,email_21,email_22,email_23,email_24,email_25,email_26,email_27,email_28,email_29,email_30]

            #### This for loop will have issues.... Assuming there are 3 emails in the POST request this for loop would try to save 3 different Campaigns (solution? "If any emaildomain in emaildomains !=: " ) something like that
            for email in emails:
                if email != False:
                    emailstr = str(email)
                    emaildomain = emailstr[emailstr.index('@') + 1 : ]
                    if emaildomain != primary_mail_domain[0]:
                        ##### could add a more unique 404 here that specifically tells the user that email addresses didnt match.
                        return render(request, "phishing/404.html")


            sendmail(campaign_id, msp_id, company_name, campaign_name, campaign_id, template_name, primary_mail_domain, emails)

            job = Campaigns(msp_id=msp_id, template_name=template_name, date=date, campaign_name=campaign_name, company_name=company_name, campaign_id=campaign_id, email_1=email_1, email_2=email_2, email_3=email_3, email_4=email_4, email_5=email_5, email_6=email_6, email_7=email_7, 
            email_8=email_8, email_9=email_9, email_10=email_10, email_11=email_11, email_12=email_12, email_13=email_13, email_14=email_14, email_15=email_15, 
            email_16=email_16, email_17=email_17, email_18=email_18, email_19=email_19, email_20=email_20, email_21=email_21, email_22=email_22, email_23=email_23, 
            email_24=email_24, email_25=email_25, email_26=email_26, email_27=email_27, email_28=email_28, email_29=email_29, email_30=email_30 )

            job.save()

            return redirect('phishing:success')

        else:
            return redirect('home:login')
    else:
        
        companies = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
        allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

        context ={
            'companies':companies,
            'allcomps':allcomps

        }
        
        return render(request, 'phishing/emailsinput.html', context)
    

@login_required(login_url='home:login')
def success(request):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps
    }
    return render(request, 'phishing/success.html', context)

def pixel(request):
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    headers = request.headers
    str_headers = str(headers)
    print(str_headers)
    whoami = request.GET.get('uid', '')
    print(whoami)
    logging.debug(whoami)
    gif_str = base64.b64decode(gif)
    logging.info("Action tracked")
    if "Referer" in headers:
        if headers["Referer"]  == 'http://mail.google.com/':
            print("ignore google")
            return HttpResponse(gif_str, content_type='image/gif')
        else:
            gotYou(whoami)
            return HttpResponse(gif_str, content_type='image/gif')
    else:
        gotYou(whoami)
    return HttpResponse(gif_str, content_type='image/gif')

@login_required(login_url='home:login')
def dashboard(request):

    campaigns = Campaigns.objects.order_by('company_name').filter(msp_id=request.user.username)
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

    context ={

        'campaigns':campaigns,
        'allcomps':allcomps
    }
    
    return render(request,"phishing/dashboard.html", context)
    
def uhoh(request):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps
    }
    return render(request, "phishing/404.html") 

@login_required(login_url='home:login')
def campaign_dashboard(request, campaign_id):
    msp_id = request.user.username

    auth_user = Campaigns.objects.filter(campaign_id=campaign_id).values('msp_id')
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    campaigns = Campaigns.objects.filter(campaign_id=campaign_id)

    ##### theres no way this is going to work....
    tracking = EmailTracking.objects.filter(campaign_id=campaign_id)

    query ={
        'campaigns':campaigns,
        'tracking':tracking,
        'allcomps':allcomps 
    }

    for x in auth_user:
        if x['msp_id'] != msp_id:
            return render(request, "phishing/404.html")
        
        else:
            return render(request, "phishing/campaign_dashboard.html", query)

