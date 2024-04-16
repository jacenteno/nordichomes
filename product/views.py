from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import MultipleObjectsReturned
from .models import Product,Review

def product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        if request.method =='POST':
           rating  = request.POST.get('rating',3)
           content = request.POST.get('content','')
           if content:
               review = Review.objects.create(
                   product=product,
                   rating=rating,
                   content=content,
                   created_by=request.user
                   
               )
               return render('product',slug=slug)
    
            
        return render(request, 'product/product.html', {'product': product})
    
    except Product.MultipleObjectsReturned:
        # Handle the case where multiple products have the same slug
        # For example, redirect to a different page or display an error message
        return render(request, 'product/multiple_products_error.html')

