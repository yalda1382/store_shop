import json
from django.shortcuts import get_object_or_404, render,redirect
from .models import Product , Category , Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
#create forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .forms import SignUpForm , UpdateUserForm , UpdatePasswordForm , UpdateUserInfo

from django.shortcuts import render
from django.db.models import Q
from .models import Product
from cart.cart import Cart
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress,Order,OrderItem

def search(request):
    results = None
    message = ''
    
    if request.method == "POST":
        query = request.POST.get('searched', '').strip()
        if query:
            results = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            if not results.exists():
                message = "No products found matching your search criteria."
            else:
                message = f"{results.count()} product(s) found."
        else:
            message = "Please enter a search term."
    
    return render(request, 'search.html', {'searched': results, 'message': message})

def category_summery(request):
    all_categories=Category.objects.all()
    return render(request,'category_summery.html',{'categories':all_categories})



def helloworld(request):
    all_products=Product.objects.all()
    return render(request,'index.html',{'products':all_products})



def about (request):
    return render(request,'about.html')



def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "you have been logged in")
            return redirect('home')

        else:
            messages.error(request, "there was an error logging in")
            return render(request, 'login.html')

    return render(request, 'login.html')



def logout_user(request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('home')




#GET → وقتی کاربر فقط صفحه رو باز می‌کنه یا اطلاعاتی می‌خواد.
#POST → وقتی کاربر داده‌ای می‌فرسته (مثلاً فرم ثبت‌نام یا لاگین).   
def signup_user(request):
    form = SignUpForm()  # فرم خالی برای GET
    if request.method == "POST":
        form = SignUpForm(request.POST)  # فرم پر شده با داده‌های کاربر
        if form.is_valid():
            user = form.save()  # کاربر ساخته می‌شود
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']

            # authenticate و login کاربر
            user = authenticate(username=username, password=password1)
            if user:
                login(request, user)
                messages.success(request, "You have successfully signed up!")
                return redirect('update_info')
            else:
                messages.error(request, "Authentication failed after signup. Try login.")
                return redirect('login')
        else:
            # فرم معتبر نیست → دوباره صفحه signup با پیام خطا
            messages.error(request, "Signup failed! Please correct the errors below.")
            return render(request, 'signup.html', {'form': form})
    else:
        # GET request → نمایش فرم خالی
        return render(request, 'signup.html', {'form': form})




    
def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})



def category(request,cat):
    cat=cat.replace("-"," ")
    try:
        category = Category.objects.get(name__iexact=cat)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})

    except:
        messages.success(request,("Category not found"))
        return redirect('home')
 
 
    
def update_user(request):
    if  request.user.is_authenticated:
        current_user = User.objects.get(pk=request.user.id)
        user_form=UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,("Profile updated successfully"))
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,("You need to login first"))
        return redirect('login')

def update_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to login first")
        return redirect('login')

    current_user = request.user

    if request.method == "POST":
        form = UpdatePasswordForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "Password updated successfully")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('update_password')

    else:
        # GET request → نمایش فرم
        form = UpdatePasswordForm(current_user)
        return render(request, 'update_password.html', {'form': form})



def update_info(request):
    if request.user.is_authenticated:

        current_user, _ = Profile.objects.get_or_create(
            user=request.user
        )

        shipping_user, _ = ShippingAddress.objects.get_or_create(
            user=request.user
        )

        user_form = UpdateUserInfo(
            request.POST or None,
            instance=current_user
        )

        shipping_form = ShippingAddressForm(
            request.POST or None,
            instance=shipping_user
        )

        if user_form.is_valid() and shipping_form.is_valid():
            user_form.save()
            shipping_form.save()
            messages.success(request, "User info updated successfully")
            return redirect('home')

        return render(
            request,
            'update_info.html',
            {
                'user_form': user_form,
                'shipping_form': shipping_form
            }
        )

    else:
        messages.error(request, "You need to login first")
        return redirect('login') 



def user_orders(request):
    if request.user.is_authenticated:
        deleverd_orders=Order.objects.filter(user=request.user,status= 'deleverd')
        other_orders=Order.objects.filter(user=request.user).exclude(status= 'deleverd')
        
        context={
            'delivered':deleverd_orders,
            'other':other_orders
        }
        return render(request, 'orders.html', context)
    else:
        messages.success(request,'dont have this page!!!')
        return redirect('home')
def order_details(request,pk):
    if request.user.is_authenticated:
        
        order=Order.objects.get(id=pk)
        items=OrderItem.objects.filter(order=pk)
        context={
            'order':order,
            'items':items
        }
        return render(request, 'order_details.html',context)
    else:
        messages.success(request,'dont have this page!!!')
        return redirect('home')
    
    
