from django.shortcuts import render

# Create your views here.
def addcompany(request):

    return render(request, 'companies/addcompany.html')