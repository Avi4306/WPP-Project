from django.http import HttpResponse
from django.shortcuts import render
import matplotlib # type:ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type:ignore
import pandas as pd
import io
import urllib, base64 

def index(request):
    return render(request, 'index.html')

def appointment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            data = request.POST.get("date")
            mail = request.POST.get('mail')
            time = request.POST.get('time')
            concern = request.POST.get('condition')

            # Put each field in a list for DataFrame
            df = pd.DataFrame({
                'name': [name],
                'date': [data],
                'mail': [mail],
                'time': [time],
                'concern': [concern]
            })

            df.to_csv("data.csv", mode='a', index=False, header=False)

            return render(request, "redirect.html")
        except Exception as e:
            return HttpResponse(f'Error: {e}')
    else:
        return render(request, "appointment.html")
def psychoeducation(request):
    return render(request,'psychoeducation.html')

def psedu(request):
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
    return render(request,'conditions.html')

def index(request):
    return render(request,'index.html')

def funzone(request):
    return render(request, 'funzone.html')

def resources(request):
    return render(request, 'resources.html')

def redirect(request):
    return render(request, 'redirect.html')
