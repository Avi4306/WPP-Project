from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import io
import urllib, base64
from django.core.mail import send_mail
from MindEase.models import datas
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from random import choice
from django.contrib.auth.decorators import login_required

def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            subject = 'Welcome to MindEase!'
            message = f"Hi {user.username},\n\nThank you for signing up with MindEase.\nWe are excited to be a part of your mental health journey!\n\nExplore, express, and heal 💬🧠"
            from_email = 'MindEase'
            to_list = [user.email]

            send_mail(subject, message, from_email, to_list, fail_silently=False)
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

@login_required(login_url='login')
def appointment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            date = request.POST.get("date")
            mail = request.user.email
            contact = request.POST.get("contact")
            time_slot = request.POST.get("time_slot")
            concern = request.POST.get("condition")

            psycologists = ["Avi Patel", "Rudra Trivedi", "Manthan Ladda", "Vishva Trivedi"]
            selected_psychologist = choice(psycologists)

            message_body = f"""Hi {request.user.username},

Your appointment has been booked successfully!

Date: {date}
Time: {time_slot}
Psychologist: {selected_psychologist}

We make sure you have a good experience.

Thank you for visiting our website."""

            subject = "Appointment Successfully Booked"

            # Save data to CSV
            df = pd.DataFrame({
                'name': [name],
                'date': [date],
                'mail': [mail],
                'contact': [contact],
                'time': [time_slot],
                'concern': [concern],
            })
            df.to_csv("data.csv", mode='a', index=False, header=False)

            # Save to database
            en = datas(name=name, email=mail, contact=contact, date=date, time=time_slot, concern=concern)
            en.save()

            from_email = 'mindease20170604@gmail.com'
            send_mail(subject, message_body, from_email, [mail], fail_silently=False)

            return render(request, 'redirect.html')

        except Exception as e:
            return HttpResponse(f'Error: {e}')
    else:
        return render(request, "appointment.html")

def psychoeducation(request):
    conditions = ['Depression', 'Anxiety', 'Bipolar', 'Schizophrenia', 'PTSD']
    people = [264, 284, 56, 24, 70]

    plt.bar(conditions, people, color="lightblue")
    plt.title('People Affected by Mental Illnesses')
    plt.xlabel("Conditions")
    plt.ylabel("Number (in thousands)")
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.read()).decode('utf-8')
    graph = f'data:image/png;base64,{image_data}'

    return render(request, 'psychoeducation.html', {'graph': graph})

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
