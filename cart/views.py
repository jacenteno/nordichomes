from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .cart import Cart
from product.models import Product

import logging

logger = logging.getLogger(__name__)

def add_to_cart(request,product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request,'cart/menu_cart.html')

def cart(request):
    cart = Cart(request)
    print(cart)
    for item in cart:
        print(item)
    return render(request,'cart/cart.html')

def success(request):
    return render(request,'cart/success.html')   


    


def update_cart(request,product_id,action):
    logger.debug(f"Product ID: {product_id}, Action: {action}")
    cart = Cart(request)
    if action == 'increment':
        cart.add(product_id,1,True)
    else:
        cart.add(product_id,-1,True)
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)
    if quantity:
        quantity= quantity['quantity']
        item = {
            'product': {
                'id': product_id,
                'name': product.name,
                'image':product.image.url,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price
            },
            'total_price':(quantity * product.price),
            'quantity' : quantity,
        }
    else:
        item=None
    print(item)
    print("Context data:", item)  # Print context data for debugging
    print("Template name:", 'cart/partials/cart_item.html')  # Print template name for debugging

    response= render(request,'cart/partials/cart_item.html',{'item':item})
    response['HX-Trigger']="update-menu-cart"
    return response
    
@login_required
def checkout(request):
    pub_key=settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request,'cart/checkout.html', {'pub_key': pub_key })

def hx_menu_cart(request):
    return render(request,'cart/menu_cart.html')    
def hx_cart_total(request):
    return render(request,'cart/partials/cart_total.html')    
    
     
    
