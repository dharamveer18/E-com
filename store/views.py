from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *



User = get_user_model()


# Create your views here.
def home(request):
    product = Product.objects.all()
    categorys = Category.objects.all()
    mult_id = [1,5,6]
    user = User.objects.filter(id__in=(mult_id))
    user2 = User.objects.filter(id__range=(1,5))
    user3 = User.objects.order_by('-id')[:3]
    user4 = User.objects.get(username='dharamveer')
    print("user>>>>>", user)
    print("user2>>>>>", user2)
    print("user3>>>>>", user3)
    print("user4>>>>>", user4)
    
    
    context = {"products": product, 'categorys':categorys}
    

    return render(request, 'home.html', context)

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
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

# def test(request):
#     user = User.objects.order_by(id__in=[1,4,3]).values()
#     print("user>>>>>", user)
#     return render(request,'home.html')

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
