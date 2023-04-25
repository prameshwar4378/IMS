from django.shortcuts import render, redirect
from .forms import CustomStaffCreationForm,Form_Financial_Year_Session
from django.contrib import messages
from Developer.models import DB_Session,CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


################### Custom Decorator Start ####################
def profile_completed(my_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.institute_code: 
            messages.warning(request,"Please Complete Your Profile")
            return redirect('/Institute/complete_your_profile/')
        return my_func(request, *args, **kwargs)
    return wrapper

def first_tour(my_func1):
    def wrapper(request, *args, **kwargs):
        if not request.user.tour_is_completed: 
            return redirect('/Institute/first_tour/')
        return my_func1(request, *args, **kwargs)
    return wrapper
################### Custom Decorator End ####################

 
def update_academic_session(request):
    name=request.user.username
    user = CustomUser.objects.get(username=name)
    user.save()
    if request.method == 'POST':
            academic_session = request.POST.get('cmb_update_academic_session')
            user.academic_session = academic_session
            user.save()
            messages.success(request, 'Session Updated Success...!.')
    return redirect('/Institute/')

@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
def home(request):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute')
    # code for update session common for all function End
    return render(request,'institute_dashboard.html')

@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
def staff_list(request):
        # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/staff_list')
    # code for update session common for all function End
    rec=CustomUser.objects.filter(is_staff=True, institute_code=request.user.institute_code,is_superuser=False)
    return render(request,'staff_list.html',{'rec':rec})

@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
def add_staff(request):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/add_staff')
    # code for update session common for all function End
    if request.method == 'POST':
        form = CustomStaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.institute_name = request.user.institute_name
            fm.institute_address = request.user.institute_address
            fm.institute_logo = request.user.institute_logo
            fm.institute_code = request.user.institute_code
            fm.save()
            form = CustomStaffCreationForm()
            messages.success(request,'Staff Added Successfully...!')
            return redirect('/Institute/add_staff/')
    else:
        form = CustomStaffCreationForm()
    return render(request,'add_staff.html', {'form': form})


@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
def manage_session(request):
    rec=DB_Session.objects.filter()
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


@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
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


@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')
def update_staff(request,id):
    # code for update session common for all function start
    if request.method=="POST":
        if 'cmb_update_academic_session' in request.POST:
            update_academic_session(request)
            return redirect('/Institute/staff_list/')
    # code for update session common for all function End
    if request.method=="POST":
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStaffCreationForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('/Institute/staff_list/')
        # return redirect('/Admin_Home/admin_vehical_records/')
    else:
        pi=CustomUser.objects.get(pk=id)
        fm=CustomStaffCreationForm(instance=pi)
    return render(request,'update_staff.html', {'form': fm})
       

@first_tour
@profile_completed
@user_passes_test(lambda user: user.is_institute)
@login_required(login_url='/login/')       
def delete_staff(request,id):
        pi=CustomUser.objects.get(pk=id)
        pi.delete()
        messages.success(request,'Profile Deleted Successfully!!!')
        return redirect('/Institute/staff_list/')

def first_tour(request): 
    return render(request,'first_tour.html')

def complete_first_tour(request):
    user = CustomUser.objects.get(id=request.user.id)
    user.tour_is_completed = True
    user.save()
    messages.success(request, 'Tour Completed Success...!.')
    return redirect('/Institute/staff_list/')




def complete_your_profile(request):
    if request.method == 'POST':
            institute_name = request.POST.get('txt_institute_name')
            institute_address = request.POST.get('txt_institute_address')
            institute_code = request.POST.get('txt_institute_code')
            institute_logo = request.FILES.get('txt_institute_logo')
            user = CustomUser.objects.get(id=request.user.id)
            user.institute_name = institute_name
            user.institute_address = institute_address
            user.institute_code = institute_code
            user.institute_logo = institute_logo
            user.save()
            messages.success(request, 'Profile Updated Success...!.')
            return redirect('/Institute/')
    return render(request,'complete_your_profile.html')
