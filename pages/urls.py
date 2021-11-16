from django.urls import path
from pages.views import AdminPanelView, HomePageView,AboutView,ContactView,ReviewPanelView, CustomerDashboard, CustomerCanceledSubscription, AddAddress


app_name = "pages"


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('admin_panel/', AdminPanelView.as_view(), name='admin_panel'),
    path('admin_panel/<status>/', AdminPanelView.as_view(), name='admin_panel'),
    path('review_panel/<int:id>', ReviewPanelView.as_view(), name='review_panel'),
    path('dashboard/', CustomerDashboard.as_view(), name='customer_dashboard'),
    path('dashboard/canceled/<sub>/', CustomerCanceledSubscription.as_view(), name='cancel_subscription'),
    path('address/', AddAddress.as_view(), name='address'),
    path('address/<id>/<pk>/<quan>/', AddAddress.as_view(), name='address'),
]