
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from models import *  
import bcrypt
from django.db.models import Q

def index(request):
    request.session.clear() 
    return render(request, ('pong/index.html'))


def process(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            request.session['name'] = request.POST['first_name']
            User.objects.create(first_name=request.POST['first_name'], username=request.POST['username'], password=hash1, play=False, rating=0, win=0,loss=0, stack=request.POST['stack'])       
            u = User.objects.get(username=request.POST['username'])
            request.session['id'] = u.id
            request.session['name'] = u.first_name
            return redirect('/dashboard')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            u = User.objects.get(username=request.POST['username'])
            request.session['id'] = u.id
            request.session['name'] = u.first_name
            return redirect ('/dashboard')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'users' : User.objects.order_by('updated_at')
        }
        return render(request, ('pong/success.html'), context)

def add(request, id):
    u = User.objects.get(id=request.session['id'])
    if u.play == True:
        errors = { 'already' : 'On waitlist already'}
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/dashboard')
    u.play = True
    u.save()
    return redirect('/dashboard')


def remove(request):
    u = User.objects.get(id=request.session['id'])
    u.play = False
    u.save()
    return redirect('/dashboard')



def accept(request, id):
    request.session['no'] = False
    u = User.objects.get(id=id)
    u.play = False
    u.save()
    n = User.objects.get(id = request.session['id'])
    n.play = False
    n.save()
    print request.session['no']
    return redirect('/gameon/{}'.format(id))


def gameon(request, id):
    if request.session['no'] == True:
        return redirect('/dashboard')
    context = {
        'opp' : User.objects.get(id=id),
        'use' : User.objects.get(id=request.session['id'])
    }
    return render(request, 'pong/gameon.html', context)


def ranking(request, win, loss):
    request.session['no'] = True
    w = User.objects.get(id = win)
    w.rating += 5
    w.win += 1
    w.save()
    l = User.objects.get(id = loss)
    l.rating -= 2
    l.loss += 1
    l.save()
    print request.session['no']
    return redirect ('/leaderboard')

def leaderboard(request):
    context = {
        'users' : User.objects.order_by('rating').reverse()
    }
    return render(request, ('pong/ranking.html'), context)


def ninjas(request):
    context = {
        'users' : User.objects.order_by('first_name')
    }
    return render(request, ('pong/ninjas.html'), context)


def profile(request, id):
    context = {
        'u' : User.objects.get(id = id),
        'messages' : Message.objects.filter(profile = id)
    }
    return render(request, ('pong/profile.html'), context)

def post_message(request, id):
    if request.method == 'POST':
        errors = Message.objects.text_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            p = User.objects.get(id =id)
            u = User.objects.get(id=request.session['id'])
            Message.objects.create(content=request.POST['mess_content'], user = u, profile = p)
        return redirect('/ninja/{}'.format(id))


def update(request, id):
    return redirect('/pong/ninja/{}'.format(request.session['id']))