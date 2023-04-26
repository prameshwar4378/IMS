from django.shortcuts import render
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import Custom_Institute_Creation_Form,login_form
from django.contrib import messages
from Institute.forms import CustomStaffCreationForm
from Developer.models import CustomUser

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    lg_form=login_form() 
    rg_form=Custom_Institute_Creation_Form()
    if request.method=='POST':
        if 'txt_sign_in_username' in request.POST: 
            username = request.POST.get('txt_sign_in_username', False)
            password = request.POST.get('txt_sign_in_password', False)
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
                lg_form=login_form()
                messages.warning(request,'Opps...! User does not exist... Please try again..!')


        if 'txt_sign_up_username' in request.POST:  
            username = request.POST.get('txt_sign_up_username', False)
            email = request.POST.get('txt_sign_up_email', False)
            password = request.POST.get('txt_sign_up_password', False)
            
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already exists!')
            else:
                create_user = CustomUser(
                    username=username,
                    email=email,
                    is_institute=True,
                )
                create_user.set_password(password)
                create_user.save() 
                messages.success(request,'Registration Successfully ...!')
                
                # Authenticate and login the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    authlogin(request, user)
                
                # Redirect the user to the appropriate page
                return redirect('/Institute/first_tour',{'user',user})
    return render(request,'login.html',{'form':lg_form,'rg_form':rg_form})


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
# fm = form_add_fees.save(commit=False)
# fm.student_class = dt.student_class
# fm.institute_code = request.user.institute_code
# form_add_fees.save()