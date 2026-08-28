
from django.urls import path
from deliveryboy import deliveryboy_views

urlpatterns = [
    path('register/', deliveryboy_views.delivery_register, name='delivery_register'),
    path('login/', deliveryboy_views.delivery_login, name='delivery_login'),
    path('logout/', deliveryboy_views.delivery_logout, name='delivery_logout'),
    path('dashboard/', deliveryboy_views.delivery_dashboard, name='delivery_dashboard'),
    path('toggle-status/', deliveryboy_views.toggle_status, name='toggle_status'),
    path('update-status/<int:order_id>/<int:new_status>/', deliveryboy_views.update_delivery_status, name='update_status'),
    path('delivery_support/',deliveryboy_views.delivery_contact,name='delivery_support'),
    path('change-password/', deliveryboy_views.delivery_change_password, name='delivery_change_password'),
    path('forgot-password/', deliveryboy_views.delivery_forgot_password, name='delivery_forgot_password_url'),
    path('reset-password/', deliveryboy_views.delivery_reset_password, name='delivery_reset_password_url'),

]