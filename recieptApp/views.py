# Importing necessary modules from Django
from django.shortcuts import render, redirect
from .models import Receipt 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth import logout

# View function to display receipts, requires user authentication
@login_required(login_url='/login/')
def receipts(request):
    if request.method == 'POST': 
        # Retrieving data from the POST request
        data = request.POST
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)

        # Creating a new Receipt object with the provided data
        Receipt.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            total=total
        )
        # Redirecting the user to the homepage
        return redirect('/')

    # Retrieving all Receipt objects from the database
    queryset = Receipt.objects.all()
    
    # Filtering receipts based on search query if provided
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))
    
    # Calculating the total sum of all receipts
    total_sum = sum(receipt.total for receipt in queryset)
    
    # Sending receipts and total sum to the template for rendering
    context = {'receipts': queryset, 'total_sum': total_sum}
    return render(request, 'receipt.html', context)

# View function to update a receipt, requires user authentication
@login_required(login_url='/login/')
def update_receipt(request, id):
    # Retrieving the Receipt object to be updated
    queryset = Receipt.objects.get(id=id)

    if request.method == 'POST':
        # Retrieving data from the POST request
        data = request.POST 
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)
        
        # Updating the fields of the Receipt object
        queryset.name = name
        queryset.price = price
        queryset.quantity = quantity
        queryset.total = total
        queryset.save()
        # Redirecting the user to the homepage
        return redirect('/')

    # Sending the receipt object to the template for rendering
    context = {'receipt': queryset}
    return render(request, 'update_receipt.html', context)

# View function to delete a receipt, requires user authentication
@login_required(login_url='/login/')
def delete_receipt(request, id):
    # Retrieving the Receipt object to be deleted
    queryset = Receipt.objects.get(id=id)
    # Deleting the receipt object
    queryset.delete()
    # Redirecting the user to the homepage
    return redirect('/')

# View function for user login page
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('receipts')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")

# View function for user registration page
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")

# View function to handle user logout
def custom_logout(request):
    logout(request)
    # Redirecting the user to the login page after logout
    return redirect('login') 

# View function to generate PDF receipts, requires user authentication
@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        # Retrieving data from the POST request
        data = request.POST 
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        total = float(price) * int(quantity)

        # Creating a new Receipt object with the provided data
        Receipt.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            total=total
        )
        # Redirecting the user to the PDF generation page
        return redirect('pdf')

    # Retrieving all Receipt objects from the database
    queryset = Receipt.objects.all()

    # Filtering receipts based on search query if provided
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))
    
    # Calculating the total sum of all receipts
    total_sum = sum(receipt.total for receipt in queryset)

    # Sending receipts and total sum to the template for rendering
    context = {'receipts': queryset, 'total_sum': total_sum}
    return render(request, 'pdf.html', context)
