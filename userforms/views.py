from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import json
import random

from stepautomationapp.models import UserData
from .models import FormsData, UserForms, ResponsesData


@login_required(login_url='/')
def userforms(request):
    all_forms = []
    userdetails = User.objects.get(username=request.user)
    forms = FormsData.objects.all()
    for form in forms:
        all_forms.append(form.formName)
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        return render(
            request,
            'create_forms.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'userforms': all_forms,
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'create_forms.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'userforms': all_forms
            }
        )


@login_required(login_url='/')
def handleForm(request):
    formName = request.POST.get('formdata')
    form = FormsData.objects.get(formName=formName)
    return HttpResponse(json.dumps({'form': form.formContent}),
                        content_type='application/json')


@login_required(login_url='/')
def processForm(request):
    form_data = str(request.POST.get('form_data'))
    form_name = request.POST.get('form_name')
    form_description = request.POST.get('form_description')
    has_files = request.POST.get('has_files')
    has_file = False
    if has_files == "true":
        has_file = True
    else:
        has_file = False
    try:
        user = UserForms.objects.get(form_user=str(request.user), form_name=form_name)
        return HttpResponse(json.dumps({'status_msg': 'NotOk'}), content_type='application/json')
    except UserForms.DoesNotExist:
        userform = UserForms.objects.create(
            form_user=str(request.user),
            form_name=form_name,
            form_description=form_description,
            form_content=form_data,
            has_files=has_file
        )
        userform.save()
        print("saved")
        form_details = UserForms.objects.get(form_user=str(request.user), form_name=form_name)
        print(form_details.has_files)
        return HttpResponse(json.dumps({'status_msg': 'Ok', 'form_id': form_details.pk}),
                            content_type='application/json')


def publishForm(request, form_id):
    form = UserForms.objects.get(id=form_id)
    if request.method == 'POST':
        response = []
        print(form.has_files)
        print(request.POST)
        if form.has_files:
            files_list = []
            print(request.FILES)
            fs = FileSystemStorage()
            for file in request.FILES:
                print(file)
                myfile = request.FILES.get(file)
                rand_number = str(random.randint(3000, 6000))
                fs.save('formfiles/' + rand_number + myfile.name, myfile)
                print("Saved")
                files_list.append('formfiles/' + rand_number + myfile.name)
            response.append(files_list)
        for data in request.POST:
            if data == 'csrfmiddlewaretoken':
                continue
            print(data, request.POST.get(data))
            response.append(request.POST.get(data))
        print(response)
        form_response = json.dumps({'response': response})
        response_data = ResponsesData.objects.create(
            form_response=form_response
        )
        form.user_responses.add(response_data)
        print("Response Saved")
        return render(
            request,
            'response_recorded.html'
        )
    else:
        print(form.has_files)
        return render(
            request,
            'publish_form.html',
            {
                'form_name': form.form_name,
                'form_description': form.form_description,
                'form': form.form_content,
                'has_file': form.has_files
            }
        )


@login_required(login_url='/')
def get_all_forms(request):
    userdetails = User.objects.get(username=request.user)
    forms = UserForms.objects.filter(form_user=str(request.user))
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        return render(
            request,
            'get_form_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'forms': forms
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'get_form_details.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'forms': forms
            }
        )


@login_required(login_url='/')
def get_form_responses(request, id):
    responses = []
    userdetails = User.objects.get(username=request.user)
    form = UserForms.objects.get(id=id)
    has_files = form.has_files
    form_name = form.form_name
    form_description = form.form_description
    print(form.user_responses.all())
    for response in form.user_responses.all():
        responses.append(json.loads(response.form_response).get('response'))
    print(responses)
    try:
        userdata = UserData.objects.get(userrelation=userdetails)
        return render(
            request,
            'view_form_responses.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/' + str(userdata.profilepic),
                'form_name': form_name,
                'form_description': form_description,
                'form_responses': responses,
                'has_files': has_files
            }
        )
    except UserData.DoesNotExist:
        return render(
            request,
            'view_form_responses.html',
            {
                'username': userdetails.username,
                'email': userdetails.email,
                'first_name': userdetails.first_name,
                'last_name': userdetails.last_name,
                'profilepic': 'https://stepsaasautomation.herokuapp.com/media/media/profilepic.png',
                'form_name': form_name,
                'form_description': form_description,
                'form_responses': responses,
                'has_files': has_files
            }
        )
