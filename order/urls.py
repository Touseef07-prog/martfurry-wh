from django.urls import path
from .views import CustomerDeliver, changeStatus


app_name = 'order'


urlpatterns = [
    path('deliver/', CustomerDeliver.as_view(), name='deliver'),
    path('deliver/<status>/', CustomerDeliver.as_view(), name='deliver'),
    path('change_delivery/<pk>/', changeStatus.as_view(), name='deliver_done'),
]