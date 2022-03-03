from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login as login_process
from django.contrib import messages

# Create your views here.
from django.shortcuts import render, redirect
from auth_app.forms import UserCreationForm
from auth_app.models import CustomUser

from django.http import HttpResponse


def register(req):
    if req.user.is_authenticated:
        return redirect('/management/listvictim/')
    if req.method == 'POST':
        print(req.POST['ic'])

        ic = req.POST['ic']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        kod_rujukan = req.POST['kod_rujukan']

        if len(ic) < 12:
            messages.error(req, 'IC Number are less than 12 digits')
            return redirect('register')
        if len(ic) > 12:
            messages.error(req, 'IC Number are greater than 12 digits')
            return redirect('register')

        ic_year = ic[0] + ic[1]
        ic_month = ic[2] + ic[3]
        ic_day = ic[4] + ic[5]

        dateformat = "%d-%m-%Y"
        current_year = datetime.now().year
        now = str(current_year)[:2]
        if int(now + ic_year) <= current_year:
            year = str((int(now + "00") + int(ic_year)))
        else:
            year = str((int(now + "00") - 100 + int(ic_year)))

        test_date = ic_day + '-' + ic_month + '-' + year
        valid_date = True
        try:
            valid_date = bool(datetime.strptime(test_date, dateformat))
        except ValueError:
            valid_date = False
        print(valid_date)
        if not valid_date:
            messages.error(req, 'Please try again with a valid IC Number')
            return redirect('register')
        if not ic.isnumeric():
            messages.error(req, 'IC Number has to be a number')
            return redirect('register')

        if password != confirm_password:
            messages.error(req, 'Passwords did not match')
            return redirect('register')
        if kod_rujukan != 'NINJAAIDKDH123':
            messages.error(req, 'Sila masukkan kod rujukan yang betul.')
            return redirect('register')
        if CustomUser.objects.filter(ic=ic).exists():
            messages.error(req, 'IC number is already exist.')
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(
                ic=ic, password=password, first_name=first_name, last_name=last_name)
        except Exception as e:
            return HttpResponse(e)
        return redirect('login')

    return render(req, 'auth_app/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/management/listvictim/')
    
    if request.method == 'POST':
        ic = request.POST['ic']
        password = request.POST['password']
        user = authenticate(request, ic=ic, password=password)
        if user is not None:
            login_process(request, user)
            return redirect('/management/dashboard/')

            ...
        else:
            # Return an 'invalid login' error message.
            messages.error(request, f'failed to login')
            return redirect('login')
    return render(request, 'auth_app/customlogin.html')
