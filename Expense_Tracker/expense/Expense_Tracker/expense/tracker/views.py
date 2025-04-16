from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import *
from django.db.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_page(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            Q(email = email) | Q(username= user_name)
        )

        if user_obj.exists():
            messages.error(request,'Error: Username or Email already exists')
            return redirect('/register')
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = user_name,
            email = email,
        )
        user_obj.set_password(password)
        user_obj.save()
    
    return render(request,'register.html')

def login_page(request):
    if request.method=="POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username= user_name)
        
        if not user_obj.exists():
            messages.error(request,'Error: Username does not exist')
            return redirect('/register')

        # if user_obj.exists():
        #     messages.error(request,'Error: Username or Email already exists')
        #     return redirect('/register')

        user_obj = authenticate(username= user_name,password= password)
        if user_obj is None:
            messages.error(request,'Error: Incorrect Password')
            return redirect('/register')
        
        login(request,user_obj)
        return redirect('/home')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    messages.error(request,"Success: Logged out")
    return redirect('/login')

#Decorator to protect the route by making mandatory to login
@login_required(login_url='/login/')
def index(request):

    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if description is None:
            messages.info(request,'Please Provide Description')
            return redirect('/')
        
        try:
            amount = float(amount)
        except Exception as e:
            messages.info(request,'Amount should be in numbers and should not be empty')
            return redirect('/')
        
        Transaction.objects.create(
            description=description,
            amount=amount,
            created_by = request.user
        )
        return redirect('/')

    context = {
        'transactions': Transaction.objects.filter(created_by = request.user),
        'income': Transaction.objects.filter(created_by = request.user).aggregate(total_balance= Sum('amount'))['total_balance'] or 0,
        'balance':Transaction.objects.filter(created_by = request.user,amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense':Transaction.objects.filter(created_by = request.user,amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0

    }
    return render(request, 'index.html',context)

@login_required(login_url='/login/')
def deleteTransaction(request,uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/','index.html')