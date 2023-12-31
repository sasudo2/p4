from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Post, Comment


def index(request):
    post_list = Post.objects.all()
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def following(request):
    return render(request, "network/following.html", {
        'id': request.user.id,
    })
    
def post(request):
    if request.method == "POST":
        pos = Post()
        pos.user = request.user
        pos.title = request.POST.get("title")
        pos.post = request.POST.get("content")
        pos.save()
        return HttpResponseRedirect(reverse('index'))
    
def get(request):
    id = int(request.GET.get("id"))
    pos = Post.objects.get(id = id)
    response = pos.to_dict(request)
    return JsonResponse(response)

def load(request):
    start = int(request.GET.get("start") or 0)
    end =  int(request.GET.get("end") or start + 9)
    f = request.GET.get("f")
    if f == "f":
        posts = Post.objects.all().order_by('date').reverse()[start:end]
        data = [post.to_dict(request) for post in posts]
        # data = []
        # for i in range(start, end + 1):
        #     try:
        #         content = Post.objects.get(id = i)
        #         data.append(content.to_dict())
        #     except ObjectDoesNotExist:
        #         break
    elif f == "t":
        following_users = request.user.following.all()

        # Filter the posts by the users that the current user is following
        posts = Post.objects.filter(user__in=following_users)[start:end+1]

        data = [post.to_dict(request) for post in posts]
        data.reverse()
    
    return JsonResponse({
        "posts": data
    })
    
def like(request):
    id = int(request.GET.get("id"))
    post = Post.objects.get(id = id)
    data = post.to_dict(request)
    if data['liked'] == True:
        post.like.remove(request.user)
        post.save()
    else:
        post.like.add(request.user)
        post.save()
        
    post = Post.objects.get(id = id)
    data = post.to_dict(request)
    return JsonResponse(data)

def profile(request, user_name):
    user = User.objects.get(username = user_name)
    response = user.to_dict(request)
    return render(request, "network/profile.html", response)

def follow(request):
    user_id = request.GET.get('id')
    user = User.objects.get(id = user_id)
    if user.followers.filter(id = request.user.id).exists():
        user.followers.remove(request.user)
        user.save()
    else:
        user.followers.add(request.user)
        user.save()
        
    user = User.objects.get(id = user_id)
    response = user.to_dict(request)
    return JsonResponse(response)

def loadPost(request):
    user_id = request.GET.get('id')
    user = User.objects.get(id = user_id)
    posts = Post.objects.filter(user = user)
    data = [post.to_dict(request) for post in posts]
    data.reverse()
    return JsonResponse({
        "posts": data
    })
    
def edit(request):
    id = request.POST.get('id')
    pos = Post.objects.get(id = id)
    pos.user = request.user
    pos.title = request.POST.get("title")
    pos.post = request.POST.get("content")
    pos.save()
    return HttpResponseRedirect(reverse('index'))
