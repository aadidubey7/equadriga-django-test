from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Item
from .forms import ItemForm
# Create your views here.

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('items')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged-in')
            return redirect('items')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'items/login.html')

    
    return render(request, 'items/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('items')
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully singed up')
            return redirect('login')
            
    context = {'form': form}

    return render(request, 'items/signup.html', context)

def userLogout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

@login_required(login_url='login')
def items(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'items/items.html', context)


@login_required(login_url='login')
def addItem(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():

            name = request.POST.get('name')
            is_item = Item.get_item_by_name(name)
            if is_item:
                messages.error(request, "This item is already exists, Kindly update the price")
                return redirect('items')
            

            form.save()
            messages.success(request, 'The item has been added')
            return redirect('items')
            
            
    context = {'form': form}
    return render(request, 'items/add-item.html', context)


@login_required(login_url='login')
def editItem(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'The item has been updated')
            return redirect('items')

    context = {'form': form}
    return render(request, 'items/add-item.html', context)


@login_required(login_url='login')
def deleteItem(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'The item has been removed successfully')
        return redirect('items')

    context = {'item': item}
    return render(request, 'items/delete-item.html', context)


@login_required(login_url='login')
def summary(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    items = Item.objects.all()
    total_price = Item.get_total_price()
    context = {'items': items, 'total_price': total_price}
    return render(request, 'items/summary.html', context)