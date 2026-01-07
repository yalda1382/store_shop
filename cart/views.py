from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from shop.models import Product




def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.prods()
    quintities = cart.get_quants()
    total = cart.get_totals()

    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'quintities': quintities,
        'total': total,
        'qty_range': range(1, 6),  # ✅ فقط 1 تا 5
    })

def cart_add(request):
    cart = Cart(request)

    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_quantity = len(cart)
        messages.success(request, 'Item added to cart successfully')
        return JsonResponse({'qty': cart_quantity})



def cart_update(request):
    cart = Cart(request)

    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)

        cart.update(product=product, quantity=product_qty)

        return JsonResponse({'qty': product_qty})


def cart_delete(request):
    cart = Cart(request)

    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        return JsonResponse({'product': product_id})


