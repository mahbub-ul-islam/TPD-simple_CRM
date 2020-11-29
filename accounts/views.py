from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import *
from .forms import OrderForm


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers, 'orders':orders,
               'total_order':total_order, 'delivered':delivered, 'pending':pending
               }
    
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_order = orders.count()
    
    context = {'customer':customer, 'orders':orders,
               'total_order':total_order}
    
    return render(request, 'accounts/customer.html', context)





def createOrder(request):

    form = OrderForm()

    if request.method == 'POST':
        #print('Printing Post : ', request.POST)
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}

    return render(request, 'accounts/order_form.html', context)












