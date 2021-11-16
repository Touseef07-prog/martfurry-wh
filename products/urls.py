from django.urls import path
from products.views import SingleProductView, BuyNow, test, test2


app_name = "product"

urlpatterns = [
    path('single_product/<int:id>', SingleProductView.as_view(), name='single_product'),
    path('Buy-Now/', BuyNow.as_view(), name='buy-now'),
    path('test/', test, name='test'),
    path('test2/<video_id>/', test2, name='test2'),
]