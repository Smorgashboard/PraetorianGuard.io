from re import L
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dashboard/dashboard.html')

def profile(request):
    return render(request, 'dashboard/profile.html')