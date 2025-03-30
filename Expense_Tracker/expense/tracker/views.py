from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import *
from django.db.models import *

# Create your views here.

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
            amount=amount
        )
        return redirect('/')

    context = {
        'transactions': Transaction.objects.all(),
        'income': Transaction.objects.all().aggregate(total_balance= Sum('amount'))['total_balance'] or 0,
        'balance':Transaction.objects.filter(amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
        'expense':Transaction.objects.filter(amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0

    }
    return render(request, 'index.html',context)

def deleteTransaction(request,uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/','index.html')