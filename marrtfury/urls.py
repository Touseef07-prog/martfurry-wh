
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include(("pages.urls",'pages') ,namespace='pages')),
    path("product/",include(("products.urls",'products'), namespace='products')),
    path("registration/",include(("registration.urls",'registration'),namespace='registration')),
    path("orders/",include(("order.urls", 'order'),namespace='order')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
