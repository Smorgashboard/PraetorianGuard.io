from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
import os
import requests
from django.contrib.auth.decorators import login_required
from users.models import Companies
from .models import OSINTS
import json
import subprocess
import time
import random
import string
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
from leakcheck import LeakCheckAPI

#### Classes (mainly for Monitoring (Watchdog))
class MonitorFolder(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_created(self, event):
        if event.src_path.endswith(".xml"):
            src = event.src_path
            time.sleep(3)
            print("stopping")
            store_harvscan(src)
            self.observer.stop()

### Start HIBP api functions

def hibp(target):
    api = (f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}")
    key = {"hibp-api-key" : ""}
    request = requests.get(api, headers=key)
    contents = request.content
    js = json.loads(contents)
    pwns = []
    for x in js:
        pwns.append(x['Name'])
    return pwns

def hibp_pastses(target):
    api = (f"https://haveibeenpwned.com/api/v3/pasteaccount/{target}")
    key = {"hibp-api-key" : ""}
    request = requests.get(api, headers=key)
    content = request.content

def hibp_pws(target):
    h = hashlib.sha1()
    target = target.encode(encoding = 'UTF-8')
    h.update(target)
    hashes = h.hexdigest()
    realtarget = hashes[:5]
    secondtarg = hashes[5:].upper()
    api = (f"https://api.pwnedpasswords.com/range/{realtarget}")
    request = requests.get(api)
    content = request.content
    string_content = content.decode("utf-8")
    lines = string_content.split("\r\n")
    pws = {}
    comped = False

    ### iterate through lines 
    for line in lines:
        key, value = line.split(":")
        pws[key] = value
    
    ### Check for match
    if secondtarg in pws:
        value = pws[secondtarg]
        print("Thats compromised!")
        print(value)
        comped = True
        return [comped, value, target]
    else:
        print("Not compromised")
        return [comped]
        
### End HIBP api functions

### Setup LeakCheckAPI  
api = LeakCheckAPI()
api.set_key("")

### Dehashed API Key 
dh_api_key = ""

### Start Leak Check API functions 

def leakCheckEmailByPass(target):
    api.set_type("pass_email")
    api.set_query(target)
    results = api.lookup()
    print(results)
    goodResults = []
    emails = []
    users = []
    if bool(results):
        print("NotEmpty")
        for result in results:
            goodResults.append(result["line"])
        for x in goodResults:
            emails.append(x.split(":")[0])
        for email in emails:
            users.append(email.split("@")[0])
        users2 = set(users)
        return [bool(results), users2]
    else:
        print("Empty")
        return [bool(results)]

def leakCheckEmail(target):
    api.set_type("email")
    api.set_query(target)
    results = api.lookup()
    danger = []
    emails = []
    pws = []
    sources = []
    if bool(results):
        for result in results:
            sources.append(result["sources"])
            source = str(result["sources"])
            if source == "['Stealer Logs']":
                danger.append(result["line"])
                try:
                    emails.append(result["line"].split(":")[0])
                    pws.append(result["line"].split(":")[1])
                except:
                    emails.append(result["line"])
            else:
                try:
                    emails.append(result["line"].split(":")[0])
                    pws.append(result["line"].split(":")[1])
                except:
                    emails.append(result["line"])
        return [bool(results), danger, emails, pws, sources]
    else:
        return [bool(results)]

def leakCheckDomain(target):
    api.set_type("domain_email")
    api.set_query(target)
    results = api.lookup()
    emails = []
    pws = []
    danger = []
    if bool(results):
        print("NotEmpty")
        for result in results:
            source = str(result["sources"])
            if source == "['Stealer Logs']":
                danger.append(result["line"])
            else:
                try:
                    emails.append(result["line"].split(":")[0])
                    pws.append(result["line"].split(":")[1])
                except:
                    emails.append(result["line"])
        return [bool(results), danger, emails, pws]
    else:
        return [bool(results)]

### Dehashed functions

def dehashedDomain(target):
    dh_api = (f"https://api.dehashed.com/search?query=domain:{target}")
    headers = {"Accept": "application/json"}
    request = requests.get(dh_api, auth= HTTPBasicAuth('email/username', dh_api_key), headers=headers)
    data = json.loads(request.content)
    emails = []
    pws = []
    addresses = []
    ips = []
    usernames = []
    booly = bool(data["entries"])
    if booly == True:
        for x in data["entries"]:
            emails.append(x["email"])
            pws.append(x["password"])
            addresses.append(x["address"])
            ips.append(x["ip_address"])
            usernames.append(x["username"])
        emails = [x for x in emails if x != '']
        pws = [x for x in pws if x != '']
        addresses = [x for x in addresses if x != '']
        ips = [x for x in ips if x != '']
        usernames = [x for x in usernames if x != '']
        return [booly, emails, pws, addresses, ips, usernames]
    else:
        print("No Results Found")
        return [booly]

### Random functions

def generate_scan_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(20))

def create_file_listener(curdir):
    ###something awesome
    src_path = curdir
    observer = Observer()
    event_handler=MonitorFolder(observer)
    observer.schedule(event_handler, path=src_path, recursive=True)
    print("Monitoring started")
    observer.start()

def run_harvest(company, target):
    os.chdir("/Users/hackintosh/harvscans/")
    ###Check if company exists (folder)
    if not os.path.exists(company):
        os.makedirs(company)
    os.chdir(company)
    curdir = os.getcwd()
    #create_file_listener(curdir)
    dt = datetime.now()
    print("Coolness would have happend now")
    #createprocess = subprocess.Popen(['theharvester', '-d', target, '-b', 'all', '-f', f'{dt}'])
    return dt

def store_harvscan(src):
    h = OSINTS.objects.get(file_name=src)
    completed = True
    h.completed = completed 

# Create your views here.
@login_required(login_url='home:login')
def dashboard(request):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps
    }
    return render(request, "OSINT/dashboard.html", context)

@login_required(login_url='home:login')
def scan_dashboard(request, scan_id):
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps
    }
    return render(request, "OSINT/scandashboard.html", context)

@login_required(login_url='home:login')
def scan(request):
    if request.method == 'POST':
        msp_id = request.user.username
        #scan_name = request.POST['scan_name']
        company_name = request.POST['company_name']
        target = request.POST['target']
        scan_type=request.POST['scan_type']
        ### this is wrongish... but not terribly wrong
        if scan_type == "email":
            hibp(target)
            lc_email_results = leakCheckEmail(target)
            return redirect('wpscan:success')
        elif scan_type == "password":
            hibp_results = hibp_pws(target)
            leakCheck_results = leakCheckEmailByPass(target)
            if hibp_results[0] == True or leakCheck_results[0] == True:
                ### cleanup before redirect
                returns2 = leakCheck_results[1]
                sendME = []
                for x in returns2:
                    sendME.append(x)
                return pwCompromised(request, hibp_results, sendME)
            return redirect('OSINT:success')
        elif scan_type == "domain":
            lc_results = leakCheckDomain(target)
            dh_results = dehashedDomain(target)
            if lc_results[0] == True or dh_results[0] == False:
                return domainCompromised(request, lc_results, dh_results)
            else:
                #### This will happen if no results are found between dehashed and leakchecker
                return redirect('OSINT:success')
        else:
            return redirect('phishing:404')
    else:
        scans = OSINTS.objects.order_by('company_name').filter(msp_id=request.user.username)
        allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

        context ={

            'scans':scans,
            'allcomps':allcomps
        }
        return render(request, "OSINT/addscan.html", context)

@login_required(login_url='home:login')
def success(request):
    canvas_html = '<canvas id="game_canvas" width="800" height="600"></canvas>'
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps,
        'cavas_html':canvas_html
    }
    return render(request, 'OSINT/success.html', context)

@login_required(login_url='home:login')
def pwCompromised(request, hibp_values, leakCheck_values):
    times = hibp_values[1]
    target = hibp_values[2]
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    context ={
        'allcomps':allcomps,
        'target':target,
        'times':times,
        'leakcheck':leakCheck_values
    }
    return render(request, 'OSINT/pwCompromised.html', context)

@login_required(login_url='home:login')
def pwScan(request):
    if request.method == 'POST':
        target = request.POST['target']
        hibp_results = hibp_pws(target)
        leakCheck_results = leakCheckEmailByPass(target)
        print(hibp_results[0])
        print(leakCheck_results[0])
        if hibp_results[0] == True or leakCheck_results[0] == True:
            ### cleanup before redirect
            returns2 = leakCheck_results[1]
            sendME = []
            for x in returns2:
                sendME.append(x)
            return pwCompromised(request, hibp_results, sendME)
        return redirect('OSINT:success')

### Start Domain Compromised views:
###STOP don't try to 'fix' this. Its redundant code I know but you need to shuffle pws before you set them  
###And you need to set in these if statments because if the functions return sets they cannot be combined 
### So don't fix anything 
@login_required(login_url='home:login')
def domainCompromised(request, lc_results, dh_results):
    ### sidebar comps navigation
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

    if lc_results[0] == True and dh_results[0] == False:
        danger = lc_results[1]
        emails = lc_results[2]
        pws = lc_results[3]
        emails = set(emails)
        random.shuffle(pws)
        pws = set(pws)
        context ={'danger':danger, 'emails':emails, 'pws':pws, 'allcomps':allcomps}
        return render(request, 'OSINT/domainCompromised.html', context)
    elif lc_results[0] == False and dh_results[0] == True:
        emails = dh_results[1]
        pws = dh_results[2]
        addresses = dh_results[3]
        ips = dh_results[4]
        users = dh_results[5]
        emails = set(emails)
        random.shuffle(pws)
        pws = set(pws)
        context ={'danger':danger, 'emails':emails, 'pws':pws, 'addresses':addresses, 'ips':ips, 'users':users, 'allcomps':allcomps}
        return render(request, 'OSINT/domainCompromised.html', context)
    elif lc_results[0] == True and dh_results[0] == True:
        danger = lc_results[1]
        emails = lc_results[2]
        pws = lc_results[3]
        random.shuffle(pws)
        dh_emails = dh_results[1]
        dh_pws = dh_results[2]
        random.shuffle(dh_pws)
        addresses = dh_results[3]
        ips = dh_results[4]
        users = dh_results[5]
        emails = emails + dh_emails
        emails = set(emails)
        pws = pws + dh_pws
        pws = set(pws)
        context ={'danger':danger, 'emails':emails, 'pws':pws, 'addresses':addresses, 'ips':ips, 'users':users, 'allcomps':allcomps}
        return render(request, 'OSINT/domainCompromised.html', context)


