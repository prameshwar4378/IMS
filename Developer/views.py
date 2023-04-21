from django.shortcuts import render
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Custom_Institute_Creation_Form,login_form
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    form=login_form()
    if request.method=='POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            authlogin(request,user)
            if user.is_superuser==True:
                return redirect('/Developer',{'user',user})
            elif user.is_institute==True:
                return redirect('/Institute',{'user',user})
            elif user.is_staff==True:
                return redirect('/Staff',{'user',user})
            elif user.is_student==True:
                return redirect('/Student',{'user',user})
        else:
            form=login_form()
            messages.error(request,'Opps...! User does not exist... Please try again..!')
    return render(request,'login.html',{'form':form})


def logout(request):
    DeleteSession(request)
    return redirect('/accounts/login')

def home(request):
    return render(request,'developer_dashboard.html')

def institute_list(request):
    return render(request,'institute_list.html')

def add_institute(request):
    if request.method == 'POST':
        form = Custom_Institute_Creation_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Institute Added Successfully ...!')
            return redirect('/Developer/add_institute/')
            # login(request, user)
    else:
        form = Custom_Institute_Creation_Form()
    return render(request, 'add_institute.html', {'form': form})