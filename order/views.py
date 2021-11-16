from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Subscription
import stripe

from env.stripee import STRIPE_PRIVATE_KEY

stripe.api_key = STRIPE_PRIVATE_KEY

# Create your views here.


class CustomerDeliver(View):
    def get(self, request, status="", *args, **kwargs):
        if status == "" or status == None:
            items = Subscription.objects.all()
            class_active = None
            action = None
        else:
            items = Subscription.objects.filter(delivery=status)
            action = status
            class_active = status

        context = {"items": items, "class_active": class_active, "action": action}
        return render(request, "order/delivery.html", context)


class changeStatus(View):
    def get(self, request, pk, *args, **kwargs):
        item = Subscription.objects.get(pk=pk)
        item.delivery = "delivered"
        item.save()

        return redirect("order:deliver")
