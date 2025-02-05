from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pyotp
import time
from qrcode import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail  
from django.conf import settings
import requests
import random
from django.http import JsonResponse
from .models import *
import qrcode
from io import BytesIO


User = get_user_model()


# Create your views here.
def home(request):
    product = Product.objects.all()
    categorys = Category.objects.all()
    search = request.POST.get('search')
    if search:
        print(search,'search valueeeeeeeeeeeeeeeeeeeeee')
        product = Product.objects.filter(productname__icontains=search)
        print(product,'product foundddddddddddd')
    else:
        print("else",search)
    
    
    context = {"products": product, 'categorys':categorys, 'search':search}
    

    return render(request, 'home.html', context)

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        print(username,'username')
        password = request.POST.get('password')
        print(password,'password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Succesful")
            return redirect('home')
        else:
         messages.error(request, "Invalid Username or Password")
         return redirect('login_page')
    
    return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            return redirect('/signup/')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('/signup/')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            profile_image=profile_image,
            phone_number=phone_number
        )

        # Display success message and redirect to login page
        messages.info(request, "Account created successfully!")
        return redirect('/login/')

    

    return render(request, 'signup.html') 
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category = Category.objects.all()
    context = {'product':product, 'category':category}
    return render(request, 'product_detail.html', context)

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        messages.success(request,'please log in to access cart')
        return redirect('login_page')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def category(request,pk):
    categorys = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(category=categorys)
    context = {'categorys': categorys, 'product': product}
    return render(request, 'category.html', context)


def buy(request):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        number=request.POST.get('number','')
        address=request.POST.get('address','')
        country=request.POST.get('country','')
        city=request.POST.get('city','')
        zip_code=request.POST.get('zip','')
        
        order=Orders(name=name,email=email,number=number,address=address,country=country,city=city,zip_code=zip_code,)
        order.save()
   
    return render(request,'buy.html')


def generate_otp(request):
    form = 'enter_otp'
    # Generate and send OTP for the user
    base32secret = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret, interval=60, digits=5)
    otp_value = otp.now()

    print(otp_value,'otpppppppppp')
    # Assuming user object is fetched somehow
    email = request.POST.get('email')
    request.session['email'] = email  
    print(request.session.items())  # To print the entire session

    print(email,'>>>>>>>>>>')
    user = User.objects.filter(email = email).first()
    print(user,'')
    if user:
        user.otp = otp_value
        user.otp_secret = base32secret
        user.save()

    send_mail(
            'Email Verification OTP',
            f'Your OTP for email verification is: {otp_value}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

    return render(request,'forget.html',{'form': form})

@csrf_exempt
def otp_verification(request):
    otp = request.POST.get('otp') 
    email = request.session.get('email')
    print(email,'email recived from user ') 
    print(otp, '>>>>>> OTP received')

    user = User.objects.filter(otp=otp).first()
    print(user, 'User retrieved after OTP check')
    if email:
        return render(request, 'reset.html')
    else:
        return JsonResponse({"message": "OTP is Invalid"})

def pass_reset(request):
    email = request.session.get('email')
    print(email,'email get from session')
    if email:
        user  = User.objects.filter(email=email).first()
        print(user,'userrrrrrrrrrrrrrr')
        new_pass = request.POST.get('pass1')
        print(new_pass)
        confirm_pass = request.POST.get('pass2')
        print(confirm_pass)

        if new_pass and confirm_pass != new_pass and confirm_pass:
            messages.error(request,'Both password has to same')
            return redirect('reset/')
        elif user.check_password(new_pass) == True :
            messages.error(request,'New Password has to be diffrent from the previous password')
            return redirect('reset/')
        else:
            user.set_password(new_pass)
            user.save()
            return redirect('login_page')

    return render(request, 'reset.html')

def forget(request):
    form = 'forget_password'
    return render(request,'forget.html',{'form':form})  

def qr_gen(request):
    if request.method == 'POST':
        data = request.POST['data']
        img = make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + '/' + img_name)
        return render(request, 'qr.html', {'img_name': img_name})
    return render(request, 'qr.html')

# def generate_qr_code(request):
#     url = request.build_absolute_uri('/product_list/')  # Change to your product page URL
#     qr = qrcode.make(url)
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     return HttpResponse(buffer.getvalue(), content_type="image/png")