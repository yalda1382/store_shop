from shop.models import Product ,Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request=request
        cart = self.session.get("session_key")

        # اگر سبد وجود نداشت، بساز
        if not cart:
            cart = self.session["session_key"] = {}

        self.cart = cart
    def db_add(self, product, quantity):
            product_id = str(product)
            product_qty = int(quantity)

            if product_id in self.cart:
                self.cart[product_id] += product_qty
            else:
                self.cart[product_id] = product_qty

            self.session.modified = True
            if self.request.user.is_authenticated:
                current_user=Profile.objects.filter(user__id=self.request.user.id)
                db_cart=str(self.cart).replace('\'','\"')
                current_user.update(old_cart=str(db_cart))
    # -------------------------
    # ADD
    # -------------------------
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # اگر محصول قبلاً بود، مقدار جدید جایگزین شود
        self.cart[product_id] = product_qty

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            db_cart=str(self.cart).replace('\'','\"')
            current_user.update(old_cart=str(db_cart))

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] = product_qty
            self.session.modified = True
        if self.request.user.is_authenticated:
                current_user=Profile.objects.filter(user__id=self.request.user.id)
                db_cart=str(self.cart).replace('\'','\"')
                current_user.update(old_cart=str(db_cart))
        return self.cart

    # -------------------------
    # DELETE
    # -------------------------
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
        if self.request.user.is_authenticated:
                current_user=Profile.objects.filter(user__id=self.request.user.id)
                db_cart=str(self.cart).replace('\'','\"')
                current_user.update(old_cart=str(db_cart))

    # -------------------------
    # GET PRODUCTS
    # -------------------------
    def prods(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    # -------------------------
    # GET QUANTITIES
    # -------------------------
    def get_quants(self):
        quantities = {}
        for key, value in self.cart.items():
            quantities[int(key)] = int(value)
        return quantities

    # -------------------------
    # TOTAL PRICE
    # -------------------------
    def get_totals(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            key = int(key)
            qty = int(value)

            for product in products:
                if product.id == key:
                    if product.Is_sale:
                        total += product.sale_price * qty
                    else:
                        total += product.price * qty

        return total

    # -------------------------
    # LENGTH
    # -------------------------
    def __len__(self):
        return len(self.cart)



