from django.shortcuts import render

# Create your views here.
def prant(request):
    print(request.headers)
    return render(request,"prant.html",{})
def home(request):
    return render(request,"home.html",{})
def base(request):
    return render(request,"base.html",{})