from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Recipe
from datetime import datetime

def main_view(request):
    # if not request.user.is_authenticated:
    #     return redirect('/splash/')
    if request.method == 'POST' and request.POST['title'] != "" and request.POST['intro'] != "" \
        and request.POST['body'] != "":
            recipe = Recipe.objects.create(
                title = request.POST['title'],
                image = request.POST['image'],
                intro = request.POST['intro'],
                ingredients = request.POST['ingredients'],
                body = request.POST['body'],
                author = request.user,
                created_at = datetime.now()
            )
            recipe.save()
    recipes = Recipe.objects.order_by('-created_at')
    return render(request, 'main.html', {'recipes': recipes})

def splash_view(request):
    return render(request, 'splash.html')

def login_view(request):
    username, password = request.POST['username'], request.POST['password']

    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

def signup_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def delete_view(request):
    recipe = Recipe.objects.get(id = request.GET['id'])
    if request.user == recipe.author:
        recipe.delete()
    return redirect('/')

def like_view(request):
    recipe = Recipe.objects.get(id = request.GET['id'])
    
    if not request.user.is_authenticated:
        return redirect('/splash')
    else:
        if len(recipe.likes.filter(username=request.user.username)) == 0:
            recipe.likes.add(request.user)
        else:
            recipe.likes.remove(request.user)
        recipe.save()
        return redirect('/')