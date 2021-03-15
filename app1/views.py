from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

def index(request):
    context = {
        "all_the_users" : User.objects.all(),
    }
    return render(request, 'index.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value, key)
        return redirect ("/")
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
                first_name = request.POST["first_name"],
                last_name = request.POST["last_name"],
                email = request.POST["email"],
                password = pw_hash,
                fecha_cumpleaños = request.POST["fecha_cumpleaños"]
            )
        request.session['userid'] = User.objects.last().id
    return redirect("/success")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
    return redirect("/")

def success(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        "usuario" : user,
        "all_messages" : Message.objects.all(),
    }
    return render(request, "success.html", context)


def logout(request):
    logged_user = []
    request.session.clear()
    return redirect("/")

def create_message(request):
    Message.objects.create(
        description = request.POST["message_description"],
        user = User.objects.get(id = request.session['userid']),
    )
    return redirect("/success")

def create_comment(request):
    id_mensaje = request.POST["which_comment"]
    Comment.objects.create(
        description = request.POST["comment_description"],
        user = User.objects.get(id = request.session['userid']),
        message = Message.objects.get(id = id_mensaje),
    )
    return redirect("/success")