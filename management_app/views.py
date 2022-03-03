from django.contrib.auth.decorators import user_passes_test
from victim_app.models import Victim
from assistance_app.models import Assistance, AssistanceType
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


def dashboard(request):
    victims = Victim.objects.all()
    assistance = Assistance.objects.all()
    assistance_types = AssistanceType.objects.all()
    total_pending = 0
    total_approval = 0
    for i in assistance:
        if i.is_approved:
            total_approval += 1
        else:
            total_pending += 1

    return render(request, 'management_app/dashboard.html',
                  {'victims': victims, 'assistance': assistance, 'assistance_types': assistance_types,
                   'total_approval': total_approval, 'total_pending': total_pending})


@login_required
def list_victim(request):
    victims = Victim.objects.all()
    return render(request, 'management_app/list_victim.html', {'victims': victims})


@login_required
def view_victim_assistance(request, id):
    victim = get_object_or_404(Victim, id=id)
    victim_assistance_list = victim.assistance_list.all()
    # update is_approved
    if request.method == 'POST':
        assistance_id = request.POST['assistance_id']
        updated_assistance = victim_assistance_list.get(id=assistance_id)
        updated_assistance.is_approved = not updated_assistance.is_approved
        updated_assistance.save()

    return render(request, 'management_app/view_victim_assistance.html',
                  {'victim': victim, 'victim_assistance_list': victim_assistance_list})


@login_required
def delete_victim_assistance(request, id):
    victim = get_object_or_404(Victim, id=id)
    if request.method == 'POST':
        assistance_id = request.POST['assistance_id']
        victim_assistance = victim.assistance_list.get(id=assistance_id)
        victim_assistance.delete()
    return redirect('view_victim_assistance', id=id)


@login_required
def edit_victim_assistance(request, victim_id, assistance_id):
    victim = get_object_or_404(Victim, id=victim_id)
    victim_assistance = victim.assistance_list.get(id=assistance_id)
    assistance_types = AssistanceType.objects.all()
    print(victim_assistance.id)
    if request.method == 'POST':
        # update assistance
        assistance_type = AssistanceType.objects.get(
            id=int(request.POST['assistance_type']))
        victim_assistance.assistance_type = assistance_type
        victim_assistance.victim_number = request.POST['victimnumber']
        victim_assistance.remark = request.POST['remark']
        victim_assistance.save()

    return render(request, 'management_app/edit_victim_assistance.html',
                  {'victim': victim, 'victim_assistance': victim_assistance, 'assistance_types': assistance_types})


@login_required
def add_victim(request):
    return render(request, 'management_app/add_victim.html')


@login_required(login_url='/login')
def edit_victim(request, id):
    victim = get_object_or_404(Victim, id=id)
    if request.method == "POST":
        name = request.POST['name']
        ic = request.POST['icNum']
        phone = request.POST["phone"]
        is_kir = str(request.POST["is_kir"])
        salary = request.POST["salary"]
        address1 = request.POST["address1"]
        address2 = request.POST["address2"]
        city = request.POST["city"]
        mukim = request.POST["mukim"]
        parlimen = request.POST["parlimen"]
        state = request.POST["state"]
        poskod = request.POST["poskod"]

        victim.name = name
        victim.ic = ic
        victim.phone = phone
        victim.is_kir = is_kir
        victim.salary = salary
        victim.address1 = address1
        victim.address2 = address2
        victim.city = city
        victim.mukim = mukim
        victim.parlimen = parlimen
        victim.state = state
        victim.poskod = poskod

        victim.save()
        respond = "Edit Successful"
        return redirect('list_victim')

    return render(request, 'management_app/edit_victim.html', context={'victim': victim})


def delete_victim(request,id):
    context = {}
    icd = get_object_or_404(Victim, id=id)
    context["victim"] = icd

    if "action" in request.GET:
        icd.delete()
        context["status"] = str(icd.name) + " Removed Successfully"
        return redirect('list_victim')
    return render(request, 'management_app/delete_victim.html', context)
