from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout 

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only



@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
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



def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {'customer':customer, 'orders':orders,
               'total_order':total_order, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=7)
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        #print('Printing Post : ', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete.html', context)






@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')
















