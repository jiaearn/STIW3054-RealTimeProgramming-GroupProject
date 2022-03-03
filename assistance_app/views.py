from django.shortcuts import get_object_or_404, render, redirect

import assistance_app.models
from victim_app.models import Victim
from .forms import AssistanceForm
from .models import Assistance, AssistanceType
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def list_assistance_type(request, id):
    assistances = Victim.objects.get(id=id).assistance_list.all()
    return render(request, 'assistance_app/list.html', {'assistances': assistances})


@login_required(login_url='/login')
def request_assistance(request, id):
    victim = get_object_or_404(Victim,id=id)
    if request.method == 'POST':
        victim_num = request.POST["victim_num"]
        assistance_type_id = int(request.POST["assistance_type"])
        remark = request.POST["remark"]
        assistance_type = AssistanceType.objects.get(id=assistance_type_id)
        print(assistance_type)
        assistance = Assistance(victim_number=victim_num, remark=remark)
        assistance.assistance_type = assistance_type
        assistance.victim = victim
        assistance.save()
    assistance_type = AssistanceType.objects.all()
    return render(request, 'assistance_app/request_assistance.html', {'victim':victim,'assistance_type': assistance_type})
