from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import UserData, UserFiles
from .models import Country


def index(request):
    if request.user.is_authenticated:
        return redirect('/steps')
    else:
        return render(
            request,
            'demo-web-studio.html',
            {}
        )


'''def handle_redirect(request, template):
    return render(
        request,
        template + '.html',
        {}
    )'''


@login_required(login_url='/login')
def delete_account(request):
    user = User.objects.get(username=request.user)
    logout(request)
    user.delete()
    return redirect('/')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        keepsignin = request.POST.get('keepsignin')
        print(keepsignin)
        try:
            users = User.objects.get(email=username)
            if check_password(password, users.password):
                login(request, users)
                return HttpResponse(json.dumps({'status_msg': 'Ok'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                    content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'Invalid Username or Password'}),
                                content_type='application/json')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            usersemail = User.objects.get(email=email)
            return HttpResponse(json.dumps({'status_msg': 'NotOk', 'msg': 'User or Email Already Exists'}),
                                content_type='application/json')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=email,
                password=password,
                email=email,
            )
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return HttpResponse(json.dumps({'status_msg': 'Ok', 'msg': 'Successfully Registered'}),
                                content_type='application/json')


@login_required(login_url='/')
def dashboard(request):
    userdetails = User.objects.get(username=request.user)
    countries = Country.objects.all()
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        print(userdata.profilepic)
        print(userdata.country)
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': userdata.address,
                'zipcode': userdata.zipcode,
                'country': userdata.country,
                'city': userdata.city,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'countries': countries,
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'account-profile.html',
            {
                'logged': True,
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'address': '',
                'zipcode': '',
                'country': False,
                'city': False,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'countries': countries
            }
        )


@permission_classes([permissions.AllowAny])
def getCities(request):
    sname = request.GET['countrydata']
    results = []
    answer = str(sname)
    selected_country = Country.objects.get(country=answer)
    cities = selected_country.city_set.all()
    for city in cities:
        results.append({'name': city.city})
    return HttpResponse(json.dumps(results), content_type='application/json')


@login_required(login_url='/')
def updateProfile(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user.id)
        userdata.country = request.POST.get('country')
        userdata.city = request.POST.get('city')
        userdata.address = request.POST.get('address')
        userdata.zipcode = request.POST.get('zipcode')
        userdata.save()
    except UserData.DoesNotExist:
        userdata = UserData.objects.create(
            userrelation=user,
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            zipcode=request.POST.get('zipcode')
        )
        userdata.save()
    return redirect('/account-profile')


@login_required(login_url='/login')
def updateProfilePic(request):
    user = User.objects.get(username=request.user)
    try:

        userdetails = UserData.objects.get(userrelation=user.id)
        userdetails.profilepic = request.FILES.get('profilepic')
        userdetails.save()
        return redirect('/account-profile')
    except UserData.DoesNotExist:
        userdetails = UserData.objects.create(
            userrelation=user,
            profilepic=request.FILES.get('profilepic'),
            address='',
            country='',
            city='',
            zipcode=''
        )
        userdetails.save()
        return redirect('/account-profile')


@login_required(login_url='/login')
def handleStepFiles(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    userdata = UserFiles.objects.filter(user=user)
    if userdata.count() == 0:
        has_files = False
    else:
        has_files = True
    print(has_files)
    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        try:
            project = UserFiles.objects.get(projectName=projectName)
            return render(
                request,
                'add_files.html',
                {
                    'username': user.username,
                    'profilepic': profilepic,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'has_files': has_files,
                    'userdata': userdata,
                    'fail': 'Project Name Already Exists'
                }
            )
        except UserFiles.DoesNotExist:
            customerName = request.POST.get('customerName')
            projectDescription = request.POST.get('projectDescription')
            userfile = UserFiles.objects.create(
                user=user,
                projectName=projectName,
                customerName=customerName,
                description=projectDescription,
                userFile=request.FILES.get('userfile')
            )
            userfile.save()
            return render(
                request,
                'add_files.html',
                {
                    'username': user.username,
                    'profilepic': profilepic,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'has_files': has_files,
                    'userdata': userdata,
                    'success': 'Updated Information Successfully'
                }
            )
    else:
        return render(
            request,
            'add_files.html',
            {
                'username': username,
                'profilepic': profilepic,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'has_files': has_files,
                'userdata': userdata,
            }
        )


@login_required(login_url='/login')
def get_project_details(request, projectName):
    userdetails = User.objects.get(username=request.user)
    data = UserFiles.objects.get(user=userdetails, projectName=projectName)
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        return render(
            request,
            'project_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'data': data,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'project_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'data': data,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
            }
        )


def aboutus(request):
    return render(
        request,
        'about.html',
        {}
    )


def contactus(request):
    return render(
        request,
        'contacts-v3.html',
        {}
    )


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')
