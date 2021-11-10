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
from rest_framework.authtoken.models import Token
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To

from .models import UserData, UserFiles, Steps,Documents
from .models import Country
from userforms.models import UserForms
from .forms import Stepsform, DocumentsForm


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


@login_required(login_url='/')
def delete_account(request):
    user = User.objects.get(username=request.user)
    UserForms.objects.filter(form_user=request.user.username).delete()
    UserFiles.objects.filter(user=user).delete()
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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
            project = UserFiles.objects.get(user=user, projectName=projectName)
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


@login_required(login_url='/')
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


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            try:
                authToken = Token.objects.get(user_id=user.id)
                return render(
                    request,
                    'password-recovery.html',
                    {
                        'fail': 'Email Already Sent to ' + email
                    }
                )
            except Token.DoesNotExist:
                token_generation = Token.objects.create(user_id=user.id)
                token_generation.save()
                authToken = Token.objects.get(user_id=user.id)
                authKey = authToken.key
                try:
                    sg = SendGridAPIClient(settings.SENDGRID_EMAIL_API)
                    message = Mail(
                        from_email=Email(settings.FROM_EMAIL),
                        to_emails=To(email),
                        subject='Password Reset For StepSaas Application',
                        html_content='<a href="https://stepsaasautomation.herokuapp.com/update-password/' + authKey + '"><input '
                                                                                                                      'type="submit" '
                                                                                                                      'value="Reset '
                                                                                                                      'Password"></a> '
                    )
                    print("Message")
                    response = sg.send(message)
                    print(response.status_code)
                    return render(
                        request,
                        'password-recovery.html',
                        {
                            'success': 'Password reset link sent to  ' + email
                        }
                    )
                except Exception:
                    return render(
                        request,
                        'password-recovery.html',
                        {
                            'fail': 'An Error Occurred '
                        }
                    )
        except User.DoesNotExist:
            return render(
                request,
                'password-recovery.html',
                {
                    'fail': 'Email Does not exists'
                }
            )
    else:
        return render(
            request,
            'password-recovery.html'
        )


def update_password(request, token):
    try:
        user_token = Token.objects.get(key=token)
        if request.method == 'POST':
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if password == cpassword:
                print(user_token)
                print(user_token.user)
                user = User.objects.get(username=user_token.user)
                user.set_password(password)
                user.save()
                user_token.delete()
                return render(
                    request,
                    'update_password.html',
                    {
                        'success': 'Password Updated',
                        'expires': False
                    }
                )
            else:
                return render(
                    request,
                    'update_password.html',
                    {
                        'fail': 'Password not Matched',
                        'expires': False
                    }
                )
        else:
            return render(
                request,
                'update_password.html',
                {'expires': False}
            )
    except Token.DoesNotExist:
        return render(
            request,
            'update_password.html',
            {'expires': True}
        )


@login_required(login_url='/')
def create_steps(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
        print(profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    if request.method == 'POST':
        form = Stepsform(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.user = request.user.username
            step.save()
            form = Stepsform()
            return render(
                request,
                'create_steps.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
        else:
            form = Stepsform()
            return render(
                request,
                'create_steps.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = Stepsform()
        return render(
            request,
            'create_steps.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
            }
        )


@login_required(login_url='/')
def display_steps(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    steps = Steps.objects.filter(user=request.user.username)
    return render(
        request,
        'display_steps.html',
        {
            'username': username,
            'profilepic': profilepic,
            'steps': steps
        }
    )


@login_required(login_url='/')
def dashboard_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    return render(
        request,
        'dashboard.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
def template_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    return render(
        request,
        'templates_page.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
def documents_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    documents = Documents.objects.filter(user=request.user.username)
    return render(
        request,
        'documents_page.html',
        {
            'username': username,
            'profilepic': profilepic,
            'documents': documents
        }
    )


@login_required(login_url='/')
def clients_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    return render(
        request,
        'clients_page.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
def cases_details(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    return render(
        request,
        'cases_page.html',
        {
            'username': username,
            'profilepic': profilepic,
        }
    )


@login_required(login_url='/')
def create_document(request):
    user = User.objects.get(username=request.user)
    try:
        userdata = UserData.objects.get(userrelation=user)
        username = user.username
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic)
    except UserData.DoesNotExist:
        profilepic = 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png'
        username = request.user
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user.username
            document.save()
            return redirect('/documents')
        else:
            return render(
                request,
                'create_documents.html',
                {
                    'username': username,
                    'profilepic': profilepic,
                    'form': form
                }
            )
    else:
        form = DocumentsForm()
        return render(
            request,
            'create_documents.html',
            {
                'username': username,
                'profilepic': profilepic,
                'form': form
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
