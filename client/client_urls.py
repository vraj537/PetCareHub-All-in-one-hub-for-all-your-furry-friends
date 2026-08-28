"""
URL configuration for petcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import client_views

urlpatterns = [
    path('home/',client_views.show,name="home"),
    path('register1/',client_views.register,name="register"),
    path('login1/',client_views.login,name="login1"),
    path('product/',client_views.product,name="product"),
    path('cart/', client_views.cart_view, name="cart"), # Updated to use new cart_view
    path('add-to-cart/<int:prod_id>/', client_views.add_to_cart, name="add_to_cart"),
    path('update-cart/<int:cart_id>/<str:action>/', client_views.update_cart, name="update_cart"),
    path('remove-cart/<int:cart_id>/', client_views.remove_cart, name="remove_cart"),
    path('move-to-wishlist/<int:cart_id>/', client_views.move_to_wishlist, name='move_to_wishlist'),
    path('product-details/<int:pk>/', client_views.product_details, name='product_details'),
    path('logout1/', client_views.logout_view, name='logout1'),
    path('checkout/', client_views.checkout, name='checkout'),
    path('checkout/<int:prod_id>/', client_views.checkout, name='checkout_single'),   
    path('add-to-wishlist/<int:prod_id>/', client_views.add_to_wishlist, name='add_to_wishlist'),
    path('my-wishlist/', client_views.wishlist_view, name='wishlist_page'),
    path('submit-review/<int:prod_id>/',client_views.submit_review, name='submit_review'),
    path('team/',client_views.team,name='team'),
    path('vet_details/<int:pk>/', client_views.vet_details, name='vet_details'),
    path('my-appointments/', client_views.my_appointments, name='my_appointments'),
    path('submit-vet-feedback/', client_views.submit_vet_feedback, name='submit_vet_feedback'),
    path('edit-profile/', client_views.edit_profile, name='edit_profile'),
    path('my-orders/', client_views.my_orders, name='my_orders'),
    path('order-success/', client_views.order_success, name='order_success'),
    path('appointment-success/', client_views.appointment_success, name='appointment_success'),  # ✅ NEW
    path('appointment-payment/', client_views.appointment_payment, name='appointment_payment'),  # ✅ NEW
    path('my-orders/', client_views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', client_views.cancel_order, name='cancel_order'),  # NEW
    path('contact/', client_views.contact, name='contact'),
    path('change-password/', client_views.client_change_password, name='client_change_password'),
    path('forgot-password/', client_views.forgot_password, name='forgot_password'),
    path('reset-password/',  client_views.reset_password,  name='reset_password'),
    path('submit-order-review/<int:prod_id>/', client_views.submit_order_review, name='submit_order_review'),
    path('adoption/', client_views.adoption, name='adoption'),
    path('developers/', client_views.developers,name='developers'),
    path('future/', client_views.future,name='future'),
]
