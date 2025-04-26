from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib # type:ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type:ignore
import pandas as pd
import io
import urllib, base64
from MindEase.models import datas
from django.core.mail import EmailMessage

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from random import choice
import imaplib
import email
import time
from MindEase.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def index(request):
    return render(request, 'index.html')

def appointment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            date = request.POST.get("date")
            mail = request.POST.get('mail')
            time_slot = request.POST.get('time')
            concern = request.POST.get('condition')
            psycologists = ["Avi Patel", "Rudra Trivedi", "Manthan Ladda", "Vishva Trivedi"]
            message_body = f"Hi {request.user.username},\n\nYour appointment has been booked successfully!\n\nDate: {date}\nTime: {time_slot}\nPsychologist: {choice(psycologists)}\n\nWe make sure you have good experience\n\nThank you for visiting our website."
        
            # Save data to CSV
            df = pd.DataFrame({
                'name': [name],
                'date': [date],
                'mail': [mail],
                'time': [time_slot],
                'concern': [concern],
            })
            df.to_csv("data.csv", mode='a', index=False, header=False)

            # Save to database
            en = datas(name=name, email=mail, date=date, time=time_slot, concern=concern)
            en.save()
            email_message = EmailMessage(
                subject='Appointment Confirmed - MindEase',
                body=message_body,
                from_email=EMAIL_HOST_USER,
                to=[mail],
            )
            email_message.send()
            # Append email to 'Sent' folder via IMAP
            msg = email.message.EmailMessage()
            msg['Subject'] = 'Appointment Confirmed - MindEase'
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = mail
            msg.set_content(message_body)

            imap_server = 'imap.gmail.com'
            imap_user = EMAIL_HOST_USER
            imap_password = EMAIL_HOST_PASSWORD  # Ensure this is securely stored

            with imaplib.IMAP4_SSL(imap_server) as imap:
                imap.login(imap_user, imap_password)
                imap.append('"[Gmail]/Sent Mail"', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
                imap.logout()

            return render(request, "redirect.html")

        except Exception as e:
            return HttpResponse(f'Error: {e}')
    else:
        return render(request, "appointment.html")

def psychoeducation(request):
    conditions = ['Depression', 'Anxiety', 'Bipolar', 'Schizophrenia', 'PTSD']
    people = [264, 284, 56, 24, 70]
    plt.bar(conditions,people,color="lightblue")
    plt.title('people Affected by Mental Illnesses')
    plt.xlabel("conditions")
    plt.ylabel("Number (in thousands)")
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.read()).decode('utf-8')
    graph = f'data:image/png;base64,{image_data}'
    return render(request, 'psychoeducation.html',{'graph':graph})

def conditions(request):
    return render(request, 'conditions.html')

def funzone(request):
    return render(request, 'funzone.html')

def resources(request):
    return render(request, 'resources.html')

def redirect_page(request):
    return render(request, 'redirect.html')

def terms(request):
    return render(request, 'terms_and_conditions.html')
def privacy_policy(request):
    return render(request, 'privacy_policy.html')
