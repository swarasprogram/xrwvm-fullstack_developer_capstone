from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

DEALERS = [
    {"id": 1, "name": "Sunflower Autos", "state": "KS", "reviews":[{"user":"alex","rating":5,"text":"Great!"}]},
    {"id": 2, "name": "Lone Star Motors", "state": "TX", "reviews":[{"user":"jane","rating":4,"text":"Good"}]},
]

def home(request):
    return render(request, "home.html", {"dealers": DEALERS})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("djangoapp:home")
    return render(request, "signup.html", {"form":form})

@csrf_exempt
def login_user(request):
    data = json.loads(request.body or "{}")
    user = authenticate(username=data.get("userName"), password=data.get("password"))
    resp = {"userName": data.get("userName")}
    if user: 
        login(request, user)
        resp["status"]="Authenticated"
    else:
        resp["status"]="Invalid credentials"
    return JsonResponse(resp)

def dealers(request):
    return render(request, "dealers.html", {"dealers":DEALERS})

def dealers_by_state(request,state):
    return render(request,"dealers.html",{"dealers":[d for d in DEALERS if d["state"].lower()==state.lower()], "state":state})

def dealer_detail(request,dealer_id):
    return render(request,"dealer_detail.html",{"dealer":next((d for d in DEALERS if d["id"]==dealer_id),None)})

@login_required
def add_review(request,dealer_id):
    dealer=next((d for d in DEALERS if d["id"]==dealer_id),None)
    if request.method=="POST":
        dealer["reviews"].append({"user":request.user.username,"rating":5,"text":request.POST.get("text")})
        return redirect("djangoapp:dealer_detail",dealer_id=dealer_id)
    return render(request,"add_review.html",{"dealer":dealer})

def cars(request):
    return render(request,"cars.html",{"makes":[]})
