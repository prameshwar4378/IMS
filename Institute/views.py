from django.shortcuts import render, redirect
from .forms import CustomStaffCreationForm,Form_Financial_Year_Session
from django.contrib import messages
from Developer.models import DB_Session
# Create your views here.

def home(request):
    return render(request,'institute_dashboard.html')

def staff_list(request):
    return render(request,'staff_list.html')

def add_staff(request):
    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CustomStaffCreationForm()
            messages.success(request,'Staff Added Successfully...!')
            return redirect('/Institute/add_staff/')
    else:
        form = CustomStaffCreationForm()
    return render(request,'add_staff.html', {'form': form})


def add_session(request):
    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CustomStaffCreationForm()
            messages.success(request,'Staff Added Successfully...!')
            return redirect('/Institute/add_staff/')
    else:
        form = CustomStaffCreationForm()
    return render(request,'add_staff.html', {'form': form})


def manage_session(request):
    rec=DB_Session.objects.all()
    if request.method == 'POST':
        form = Form_Financial_Year_Session(request.POST)
        if form.is_valid():
            form.save()
            form = Form_Financial_Year_Session()
            messages.success(request,'Session Added Successfully...!')
            return redirect('/Institute/manage_session/')
    else:
        form = Form_Financial_Year_Session() 
    return render(request,'manage_session.html', {'form_add_session': form,'rec':rec})


def update_session(request,id):
    if request.method=="POST":
        pi=DB_Session.objects.get(pk=id)
        fm=Form_Financial_Year_Session(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Session Updated Successfully')
            return redirect('/Institute/manage_session/')
        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=DB_Session.objects.get(pk=id)
        fm=Form_Financial_Year_Session(instance=pi)
    return render(request,'update_session.html', {'form': fm})
       
def delete_session(request,id):
        pi=DB_Session.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Session Deleted Successfully!!!')
        return redirect('/Institute/manage_session/')


       