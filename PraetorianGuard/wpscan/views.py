from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users import views
import os
from subprocess import Popen, PIPE
import json
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler  
import logging
import time
from .models import Scans
from users.models import Companies
from wpscan_out_parse import WPScanJsonParser
from wpscan_out_parse import parse_results_from_file
import wpscan_out_parse
import random
import string

#### Classes (mainly for Monitoring (Watchdog))
class MonitorFolder(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_modified(self, event):
        if event.src_path.endswith(".json"):
            src = event.src_path
            time.sleep(3)
            parser(src)
            print("stopping")
            time.sleep(3)
            store_wpscan(src)
            self.observer.stop()

##### Non View Functions
def parser(file_loc):
    with open (file_loc, 'r') as wpscan_out:
        p = WPScanJsonParser(json.load(wpscan_out))
        finds = p.get_core_findings()
        alerts = p.get_alerts()
        sum = p.get_summary_list()
        sumLine = p.get_summary_line()
        resu = p.get_results()
        warns = p.get_warnings()
        info = p.get_infos()
        errors = p.get_error()
        s = Scans.objects.get(file_name=file_loc)
        s.finds = finds
        s.alerts = alerts
        s.sum = sum
        s.sum_line = sumLine
        s.resu = resu
        s.warns = warns
        s.info = info
        vulns = []
        for x in sum:
            if x['Vulnerabilities'] != '0':
                vulns.append(x)
        if errors != None:
            s.errors = errors
        if vulns != None:
            s.vulns = vulns
        
        ##### Save changes to DB
        s.save()
        

def store_wpscan(src):
    s = Scans.objects.get(file_name=src)
    completed = True
    s.completed = completed
    
    s.save()

def generate_scan_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(24))

def create_file_listener(curdir):
    ###something awesome
    src_path = curdir
    observer = Observer()
    event_handler=MonitorFolder(observer)
    observer.schedule(event_handler, path=src_path, recursive=True)
    print("Monitoring started")
    observer.start()

def create_scan_file(company, target):
    os.chdir("/Users/hackintosh/wpscans/")
    ###Check if company exists (folder)
    if not os.path.exists(company):
        os.makedirs(company)
    os.chdir(company)
    curdir = os.getcwd()
    create_file_listener(curdir)
    dt = datetime.now()
    createprocess = subprocess.Popen(['wpscan', '--url', target, '--output', f'{dt}.json', '--format', 'json', '--api-token', ''])
    return dt

# Create your views here.
@login_required(login_url='home:login')
def dashboard(request):
    scans = Scans.objects.order_by('company_name').filter(msp_id=request.user.username)
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

    context ={

        'scans':scans,
        'allcomps':allcomps
    }
    return render(request, "wpscan/dashboard.html", context)

@login_required(login_url='home:login')
def scan(request):
    if request.method == 'POST':
        msp_id = request.user.username
        scan_name = request.POST['scan_name']
        company_name = request.POST['company_name']
        target = request.POST['target']
        scan_id = generate_scan_id()
        dt = create_scan_file(company_name, target)
        curdir = os.getcwd()
        filename = f'{curdir}/{dt}.json'
        
        ### acutally save it this time
        scan = Scans(msp_id=msp_id, scan_name=scan_name, company_name=company_name, target=target, scan_id=scan_id, file_name=filename)

        scan.save()

        return redirect('wpscan:success')
    else:
        scans = Scans.objects.order_by('company_name').filter(msp_id=request.user.username)
        allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

        context ={

            'scans':scans,
            'allcomps':allcomps
        }
        return render(request, "wpscan/addscan.html", context)

@login_required(login_url='home:login')
def scans_dashboard(request, scan_id):
    msp_id = request.user.username

    #### CONTEXT
    auth_user = Scans.objects.filter(scan_id=scan_id).values('msp_id')
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    scans = Scans.objects.filter(scan_id=scan_id)
    s = Scans.objects.get(scan_id=scan_id)
        #### I think a little more parsing is in order 
    file_loc = s.file_name
    with open (file_loc, 'r') as wpscan_out:
        p = WPScanJsonParser(json.load(wpscan_out))
        alerts = p.get_alerts()
        warns = p.get_warnings()
        info = p.get_infos()
        errors = p.get_error()
        sums = p.get_summary_list()
        sumLine = p.get_summary_line()


    sumalerts = sumLine.split(" ")[3]
    sumwarns = sumLine.split(" ")[4]
    suminfo = sumLine.split(" ")[5]
    sumerror = sumLine.split(" ")[6]

    context = {
        'allcomps':allcomps,
        'scans':scans,
        'alerts':alerts,
        'warns':warns,
        'info':info,
        'errors':errors,
        'sumalerts':sumalerts,
        'sumwarns':sumwarns,
        'suminfo':suminfo,
        'sumerror':sumerror,
        'sums':sums

    }

    for x in auth_user:
        if x['msp_id'] != msp_id:
            return render(request, "phishing/404.html")
        
        else:
             return render(request, "wpscan/scans_dashboard.html", context)

@login_required(login_url='home:login')
def success(request):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps
    }
    return render(request, 'wpscan/success.html', context)


@login_required(login_url='home:login')
def htmlresults(request, scan_id):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    scans = Scans.objects.filter(scan_id=scan_id)
    results = parse_results_from_file('/Users/hackintosh/wpscans/Soteria/test3.json')
    html = wpscan_out_parse.format_results(results,'html')
    
    
    context ={
        'allcomps':allcomps,
        'scans':scans,
        'html':html
    }
    return render(request, 'wpscan/htmlresults.html', context)