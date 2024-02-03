from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import Companies
import random
import string
import dns.resolver
import json

def generateDNSverification ():
    randomtxt = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
    txt = 'pg=' + randomtxt
    return(txt)

# Create your views here.
@login_required(login_url='home:login')
def home(request):
    print(request.user.username)
    companies = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    print(companies)
    context ={

        'companies':companies,
        'allcomps':allcomps
    }
    print(context)
    return render(request,"users/dashboard.html", context)

@login_required(login_url='home:login')
def addcompany(request):
    if request.method == 'POST':
        msp_id = request.user.username
        company_name = request.POST['company_name']
        company_domain = request.POST['website']
        public_ip = request.POST['public_ip']
        primary_mail_domain = request.POST['primary_mail_domain']
        verification = generateDNSverification()
        print(company_name)
        if company_name != None:
            if Companies.objects.filter(company_name = company_name).exists():
                return home(request)
            else:
                Companies.objects.create(msp_id=msp_id, company_name=company_name,company_domain=company_domain, public_ip=public_ip, primary_mail_domain=primary_mail_domain, verification=verification)
                return home(request)
        else:
            return home(request)
    else:
        allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

        context = {
        'allcomps':allcomps
    }
        return render(request, "users/addcompany.html", context) 


def register(request):
    if request.method == 'POST':
        #register User
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That Email is in use already!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    #login after register
                    auth.login(request, user)
                    messages.success(request, "You are now logged in")
                    return redirect('index')
        else:
            messages.error(request, 'You fool! Your passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        #login user
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home:home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')


@login_required(login_url='home:login')
def comp_dashboard(request, id):
    msp_id = request.user.username
    auth_user = Companies.objects.filter(id=id).values('msp_id')
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)
    companies = Companies.objects.filter(id=id)

    query ={
        'companies':companies,
        'allcomps':allcomps
    }

    for x in auth_user:
        if x['msp_id'] != msp_id:
            return render(request, "phishing/404.html")
        
        else:
            return render(request, "users/compdashboard.html", query)

@login_required(login_url='home:login')
def delete_comp(request, id):
    if request.method == 'POST':
        msp_id = request.user.username
        auth_user = Companies.objects.filter(id=id).values('msp_id')

        for x in auth_user:
            print(x['msp_id'])
            if x['msp_id'] != msp_id:
                return render(request, "phishing/404.html")
            else:
                recordToDelete = Companies.objects.get(id=id)
                recordToDelete.delete()
                return home(request)

@login_required(login_url='home:login')
###### Check this ... I dont like that its only filtering by company id, could be IDOR?!
def verification(request, id):
    msp_id = request.user.username
    auth_user = Companies.objects.filter(id=id).values('msp_id')
    companies = Companies.objects.filter(id=id)
    allcomps = Companies.objects.order_by('company_name').filter(msp_id=request.user.username)

    context ={

        'companies':companies,
        'allcomps':allcomps
    }
    for x in auth_user:
            print(x['msp_id'])
            if x['msp_id'] != msp_id:
                return render(request, "phishing/404.html")
            else:
                return render(request, 'users/verification.html', context)

@login_required(login_url='home:login')
def checkDNSverification (request):
    if request.method == 'GET': 
        domain = request.GET.get('param_first')
        #### Swap this to challenge after testing
        challenge = request.GET.get('param_second')
        dnsrecords = []
        dnsrecords = dns.resolver.resolve(domain, 'txt').response.answer[0]
        for d in dnsrecords:
            dstr = str(d)
            if dstr == challenge:
                print("DNS!")
                c = Companies.objects.get(primary_mail_domain=domain)
                c.is_verified = True
                c.save()
                response = "True"
                return HttpResponse(
                    json.dumps(response),
                    content_type="application/json"
                )
        else:
            print("No DNS")
            response = "False"
            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )
