import json
import stripe
from django.http import JsonResponse

from django.conf import settings

from django.shortcuts import render,redirect

from .models import Order, OrderItem

from cart.cart import Cart

# Create your views here.
def start_order(request): 
    cart = Cart(request)
    data = json.loads(request.body)
    print(data)
    total_price =0
        
    items=[]
        
    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])
        items.append( {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name': product.name,
                    },
                    
                    'unit_amount': int(product.price )* 100,
                },
                'quantity':item['quantity'],
        })
    payment_intent='' 
    print( items)
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    print(stripe.api_key)
        #STRIPE_API_KEY_PUBLISHABLE
        #STRIPE_API_KEY_HIDEEN
        
    """
        4000005910000000
        
        -d “payment_method_types[]”=bancontact\
        -d “payment_method_types[]”=card\
        -d “payment_method_types[]”=eps\
        -d “payment_method_types[]”=giropay\
        -d “payment_method_types[]”=ideal\
        -d “payment_method_types[]”=p24\
        -d “payment_method_types[]”=sepa_debit\
    """
    session=stripe.checkout.Session.create(
            payment_method_types=[ "card"],
            line_items=items,
            mode="payment",
            success_url="http://127.0.0.1:8000/cart/success/",
            cancel_url="http://127.0.0.1:8000/cart/",
    )
    payment_intent= session.payment_intent
 
    order = Order.objects.create(
        user=request.user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],  
        address=data['address'],
        zipcode=data['zipcode'],
        place=data['place'],
        payment_intent= payment_intent,
        paid=True,
        paid_amount=total_price
        
    )
   
    order.save()
    print(order)
    """ es solo para pos sin strike
        if  request.method == 'POST':
            # Get the user information
            """"""
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            zipcode = request.POST.get('zipcode')
            place = request.POST.get('place')
            phone= request.POST.get('phone')
            order = Order.objects.create(user=request.user,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        phone=phone,
                                        address=address,zipcode=zipcode,place=place)
    
            for item in cart:
                product=item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                item = OrderItem.objects.create(order=order,product=product,price=price,quantity=quantity)
            return redirect('myaccount') 
    """  
        
    for item in cart:
        product=item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity
        item = OrderItem.objects.create(order=order,product=product,price=price,quantity=quantity)
    cart.clear()
    return JsonResponse({'session':session,'order': payment_intent})
  