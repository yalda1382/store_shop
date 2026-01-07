from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from shop.models import Product,Profile


def payment_success(request):
    return render(request, 'payment/payment_success.html')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.prods()
    quantities = cart.get_quants()
    total = cart.get_totals()

    if request.user.is_authenticated:
        shipping_user, created = ShippingAddress.objects.get_or_create(
            user=request.user
        )
        shipping_form = ShippingAddressForm(
            request.POST or None,
            instance=shipping_user
        )
    else:
        shipping_form = ShippingAddressForm(request.POST or None)

    return render(request, 'payment/checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'total': total,
        'shipping_form': shipping_form
    })


def confirm_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.prods()
        quantities = cart.get_quants()
        total = cart.get_totals()

        request.session['user_shipping'] = request.POST

        return render(request, 'payment/confirm_order.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_info': request.POST
        })

    messages.error(request, 'Invalid request')
    return redirect('home')


def process_order(request):
    if request.method != 'POST':
        messages.error(request, 'خطا در ثبت سفارش')
        return redirect('home')

    cart = Cart(request)
    cart_products = cart.prods()
    quantities = cart.get_quants()
    total = cart.get_totals()

    user_shipping = request.session.get('user_shipping', {})

    full_name = user_shipping.get('shipping_full_name', '')
    email = user_shipping.get('shipping_email', '')

    full_address = (
        f"{user_shipping.get('shipping_address1','')}\n"
        f"{user_shipping.get('shipping_address2','')}\n"
        f"{user_shipping.get('shipping_city','')}\n"
        f"{user_shipping.get('shipping_state','')}\n"
        f"{user_shipping.get('shipping_zipcode','')}\n"
        f"{user_shipping.get('shipping_country','')}"
    )

    # ساخت سفارش
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name,
        email=email,
        shipping_address=full_address,
        amount_paid=total,
    )

    # ساخت آیتم‌های سفارش
    for product in cart_products:
        quantity = quantities.get(product.id, 1)
        price = product.sale_price if product.Is_sale else product.price

        OrderItem.objects.create(
            order=order,
            product=product,
            user=request.user if request.user.is_authenticated else None,
            quantity=quantity,
            price=price,
        )
    cu=Profile.objects.filter(user__id=request.user.id)
    cu.update(old_cart=" ")

    # پاک کردن اطلاعات shipping از session
    if 'user_shipping' in request.session:
        del request.session['user_shipping']

    messages.success(request, 'سفارش با موفقیت ثبت شد')
    return redirect('home')
