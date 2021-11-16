from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from pages.models import Review
from products.models import Category, Product
from registration.models import CustomUser
from order.models import Subscription
from django.utils import timezone
from pages.forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import stripe
from env.stripee import STRIPE_PRIVATE_KEY


stripe.api_key = STRIPE_PRIVATE_KEY


# Create your views here.
# def home(request):
#     return render(request, "pages/home.html")


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        get_5cl = Category.objects.get(name="5cl")
        get_70cl = Category.objects.get(name="70cl")

        prd_5cl = Product.objects.filter(category=get_5cl)
        prd_70cl = Product.objects.filter(category=get_70cl)
        for i in prd_70cl:
            print(i.product_name)

        context = {
            "product_1": prd_5cl,
            "product_2": prd_70cl,
        }
        if request.user.is_staff:
            return redirect("pages:admin_panel")
        return render(request, "pages/home.html", context=context)


class AboutView(View):
    def get(self, request, *args, **kwargs):

        return render(request, "pages/about.html")


class ContactView(View):
    def get(self, request, *args, **kwargs):
        context = {"review_form": ReviewForm()}

        return render(request, "pages/contact.html", context=context)

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pages:home")

        context = {
            "review_form": form,
        }
        return render(request, "pages/contact.html", context=context)


class AdminPanelView(LoginRequiredMixin, View):
    login_url = "/registration/"

    def get(self, request, status="", *args, **kwargs):
        if request.user.is_superuser:
            if status == "" or status == None:
                subscription = stripe.Subscription.list(status="all")
            else:
                subscription = stripe.Subscription.list(status=status)

            required_subscription_data = []
            for s in subscription:
                single_subscription_item = {
                    "collection_method": s.collection_method,
                    "interval": s.plan.interval,
                    "product": Product.objects.get(product_stripe_id=s.plan.product),
                    "current_period_start": datetime.datetime.fromtimestamp(
                        float(s.current_period_start)
                    ),
                    "current_period_end": datetime.datetime.fromtimestamp(
                        float(s.current_period_end)
                    ),
                    "amount": s.plan.amount / 100,
                    "quantity": s.quantity,
                    "total": (s.plan.amount / 100) * (s.quantity),
                    "status": s.status,
                }

                required_subscription_data.append(single_subscription_item)

            context = {
                "subscription": required_subscription_data,
                "class_active": status,
            }

            return render(request, "pages/admin_dashboard.html", context)

        else:
            return HttpResponseRedirect(reverse("/"))


class ReviewPanelView(View):
    def get(self, request, id, *args, **kwargs):
        get_review = Review.objects.get(id=id)
        context = {"get_review": get_review}

        return render(request, "pages/review.html", context=context)


class CustomerDashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        stripe_user_id = user.stripe_id
        subscription = stripe.Subscription.list(customer=stripe_user_id, status="all")

        required_subscription_data = []
        for s in subscription:
            single_subscription_item = {
                "id": s.id,
                "collection_method": s.collection_method,
                "interval": s.plan.interval,
                "product": Product.objects.get(product_stripe_id=s.plan.product),
                "current_period_start": datetime.datetime.fromtimestamp(
                    float(s.current_period_start)
                ),
                "current_period_end": datetime.datetime.fromtimestamp(
                    float(s.current_period_end)
                ),
                "amount": s.plan.amount / 100,
                "quantity": s.quantity,
                "total": (s.plan.amount / 100) * (s.quantity),
                "status": s.status,
                "address": s.metadata,
            }

            required_subscription_data.append(single_subscription_item)

        context = {"subscription": required_subscription_data}

        return render(request, "pages/customer_dashboard.html", context)


class CustomerCanceledSubscription(LoginRequiredMixin, View):
    def get(self, request, sub, *args, **kwargs):

        stripe.Subscription.delete(sub)

        return HttpResponseRedirect("/dashboard")


class AddAddress(View):
    def get(self, request, id, pk, quan, *args, **kwargs):

        context = {
            "id": id,
            "pk": pk,
            "quan": quan,
        }

        return render(request, "pages/customer_address.html", context)

    def post(self, request, *args, **kwargs):
        checkout_exists = False

        name = request.POST.get("name")
        country = request.POST.get("country")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        contact = request.POST.get("contact")
        sub_id = request.POST.get("sub_id")
        prod_id = request.POST.get("prod_id")
        prod_quan = request.POST.get("prod_quan")

        try:
            checkout = stripe.checkout.Session.retrieve(sub_id)
            checkout_exists = True
            print("Checkout exists? ", checkout_exists)

            if checkout_exists == True:
                sub_id = checkout.subscription
        except:
            print("Checkout exists? ", checkout_exists)

        stripe.Subscription.modify(
            sub_id,
            metadata={
                "name": name,
                "country": country,
                "address_1": address_1,
                "address_2": address_2,
                "city": city,
                "state": state,
                "city": city,
            },
        )

        Subscription.objects.create(
            user=request.user,
            name=name,
            country=country,
            address_1=address_1,
            address_2=address_2,
            city=city,
            state=state,
            contact=contact,
            sub_id=sub_id,
            date=timezone.now(),
            product=Product.objects.get(pk=prod_id),
            quantity=prod_quan,
        )

        return HttpResponseRedirect("/dashboard")
