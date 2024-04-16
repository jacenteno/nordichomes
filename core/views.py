from django.contrib.auth import login # ojo
from django.contrib.auth.decorators  import login_required # ojo

from django.db.models import Q 
from django.shortcuts import render,redirect

from product.models import Product, Category

from  .forms import SignUpForm

def signup(request): 
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('/')
    else:
        form=SignUpForm()     
    return render(request,'core/signup.html',{'form': form})

@login_required    
def myaccount(request):
    return render(request,'core/myaccount.html')

@login_required    
def edit_myaccount(request):
    if request.method == "POST":
        # Get the current user
        user = request.user 

        # Update user data from POST request
        user.first_name = request.POST.get('first_name', '')  # Use get() with default value to avoid None
        user.last_name = request.POST.get('last_name', '')    # Use get() with default value to avoid None
        user.username = request.POST.get('username', '')      # Use get() with default value to avoid None
        email = request.POST.get('email', '')                 # Use get() with default value to avoid None

        # Check if email is provided
        if email:
            user.email = email
            user.save()
            return redirect('myaccount')
        else:
            # If email is not provided, render the form again with an error message
            error_message = "Email field is required."
            return render(request, 'core/edit_myaccount.html', {'error_message': error_message})

    return render(request, 'core/edit_myaccount.html')
    
# Create your views here.

def frontpage(request):
    products= Product.objects.all()[0:8]
    return render(request,'core/frontpage.html',{'products':products})
@login_required  
def shop(request):
    categories = Category.objects.all() 
    products = Product.objects.all()
     
    active_category = request.GET.get('category','')
    
    if active_category:
        products = products.filter(category__slug=active_category)
    
    query = request.GET.get('query','')
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    contexto={
        'categories':categories,
        'products':products,
        'active_category': active_category
        
    }
    return render(request,'core/shop.html',contexto)


