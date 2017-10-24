from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import User
from django.contrib import messages


def logout(request):
    request.session.flush()
    return redirect('/')

def index(request):
    return render(request, 'oct_app/index.html')

def register(request):
    results = User.objects.registerVal(request.POST)  #THIS IS PASS THE FUNCTION IN USERMANAGER. IN MODELS, THE FUNCTION REGISTERVAL IS NOW EXPECTING TWO BUT PASSING ONE
    #when we have the object return. we wanna store what's being returned in a variable. In this case, resultts
    if results['status'] == False:  #if all the results are false then user can create
        User.objects.createUser(request.POST)  #we are using request.POST to pass form data TO the function
        messages.success(request, "Your user name has been created. Please log in")
    else: 
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/')

def login(request):
    results = User.objects.loginVal(request.POST)
    if results['status'] == True:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/') #this is under the for loop 
    else:
        request.session['first_name'] = results['user'].first_name
        request.session['id'] = results['user'].id
        request.session['email'] = results['user'].email
        return redirect('/dashbord')