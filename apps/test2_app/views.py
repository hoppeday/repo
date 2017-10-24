from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import Pet
from ..oct_app.models import User
from django.contrib import messages

def index(request):
    if 'id' not in request.session: #this is to make sure no one can add a pet without bein logged in 
        return redirect('/')
    context = {
        'person': User.objects.get(id = request.session['id']),
        'users': User.objects.exclude(id = request.session['id']),  #we wanna exclude the current logged in user and we wanna extract everyone who is assigned an id to appear on the dashboard. 
    }
    return render(request, 'test2_app/index.html', context)

def add(request):
    if 'id' not in request.session: #this is to make sure no one can add a pet without bein logged in 
        return redirect('/')
    return render(request, "test2_app/add.html")

def create(request):
    if 'id' not in request.session: #this is to make sure no one can add a pet without bein logged in 
        return redirect('/')
    results = Pet.objects.validate(request.POST)
    if results['status'] == True:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/dashbord/add') 

    Pet.objects.create(name = request.POST['name'], pet_type = request.POST['pet_type'], user = User.objects.get(id=request.session['id']))
    return redirect('/dashbord')


def userpage(request, id):
    if 'id' not in request.session: #this is to make sure no one can add a pet without bein logged in 
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'test2_app/userpage.html', context)

def delete(request, id):
    if 'id' not in request.session: #this is to make sure no one can add a pet without bein logged in 
        return redirect('/dashbord')
    if request.session['id'] != Pet.objects.get(id=id).user.id:  #this is to prevent someone from deleting another users animal
        return redirect('/dashbord')
    Pet.objects.get(id=id).delete()
    return redirect('/dashbord')

