from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def appointment(request):
    return render(request,"appointment.html")

def chatbot(request):
    return render(request,'chatbot.html')

def conditions(request):
    return render(request,'conditions.html')

def index(request):
    return render(request,'index.html')

def funzone(request):
    return render(request,'funzone.html')

def redirect(request):
    return render(request,'redirect.html')
