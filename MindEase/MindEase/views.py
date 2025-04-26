from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib # type:ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type:ignore
import pandas as pd
import io
import urllib, base64
from MindEase.models import datas
from django.core.mail import send_mail

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

def signupPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
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

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def index(request):
    return render(request, 'index.html')

def appointment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            date = request.POST.get("date")
            mail = request.POST.get('mail')
            time = request.POST.get('time')
            concern = request.POST.get('condition')
            messages = f"Your AppointMent is ConForMed be Ready on {date} on time {time},Thankyou for visiting our Website." 
            # Put each field in a list for DataFrame
            df = pd.DataFrame({
                'name': [name],
                'date': [date],
                'mail': [mail],
                'time': [time],
                'concern': [concern]
            })

            df.to_csv("data.csv", mode='a', index=False, header=False)
            
            en=datas(name=name, email=mail, date=date, time=time, concern=concern)
            en.save()
            
            send_mail(
            subject='Appointment Confirmation',
            message=messages,
            from_email=f'{mail}',
            recipient_list=[mail],
            fail_silently=False,
            )
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

def redirect(request):
    return render(request, 'redirect.html')

def terms(request):
    return render(request, 'terms_and_conditions.html')
def privacy_policy(request):
    return render(request, 'privacy_policy.html')