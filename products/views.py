from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from products.models import Category, Product
from registration.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe
from env.stripee import STRIPE_PRIVATE_KEY

stripe.api_key = STRIPE_PRIVATE_KEY


# Create your views here.
class SingleProductView(View):
    def get(self, request, id, *args, **kwargs):
        get_product = Product.objects.get(id=id)
        if get_product.category.name == "5cl":
            get_category = Category.objects.get(name="5cl")
            get_related = Product.objects.filter(category=get_category)
        if get_product.category.name == "70cl":
            get_category = Category.objects.get(name="70cl")
            get_related = Product.objects.filter(category=get_category)
        context = {"product": get_product, "related": get_related}
        return render(request, "products/product_view.html", context=context)


class BuyNow(LoginRequiredMixin, View):
    login_url = "/registration/"

    def post(self, request, *args, **kwargs):
        quantity = request.POST.get("buy-now")
        product = request.POST.get("product_id")
        get_product = Product.objects.get(pk=product)

        user = CustomUser.objects.get(email=request.user)

        stripe_user_id = user.stripe_id
        stripe_price_id = get_product.product_price_id
        # amount          = int(get_product.price*100)

        # 4242 4242 4242 4242 -- Fake card to test the checkout session

        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
            # customer_email=self.request.user.email,
            customer=stripe_user_id,
            # billing_address_collection='required',
            # shipping_address_collection={
            #   'allowed_countries': ['US', 'CA'],
            # },
            line_items=[
                {
                    "price": stripe_price_id,
                    "quantity": quantity,
                },
            ],
            payment_method_types=[
                "card",
            ],
            # mode='payment',   # for one time payment
            mode="subscription",
            success_url=YOUR_DOMAIN
            + f"address/{{CHECKOUT_SESSION_ID}}/{product}/{quantity}",
            cancel_url=YOUR_DOMAIN + "cancel/",
        )

        return redirect(checkout_session.url, code=303)
        # return HttpResponseRedirect(reverse('pages:address', kwargs={'id': checkout_session.id, 'pk':product, 'quan':quantity}))

        # ret = stripe.Subscription.retrieve("sub_1JrpvKG9cGd6yAftJUwDGVX9")
        # print(ret)


def test(request):
    item = stripe.checkout.Session.list()
    j = 0
    for i in item:
        j += 1
        print(j, ":", i.subscription)

    # return HttpResponseRedirect(reverse('product:test2', kwargs={'video_id': 123}))


def test2(request, video_id):
    print(video_id)
