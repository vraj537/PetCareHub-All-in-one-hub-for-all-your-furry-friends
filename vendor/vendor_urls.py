
from django.urls import path
from vendor import vendor_views

urlpatterns = [
    path('register/',vendor_views.vendor_register,name='vendor_register'),
    path('login/', vendor_views.vendor_login, name='vendor_login'),
    path('dashboard/', vendor_views.vendor_dashboard, name='vendor_dashboard'),
    path('logout/', vendor_views.vendor_logout, name='vendor_logout'),
    path('vendor/db-status/<int:db_id>/<int:new_status>/', vendor_views.update_db_status, name='db_status'),
    path('vendor/assign-order/', vendor_views.assign_order, name='assign_order'),
    path('vendor/update-qty/<int:prod_id>/', vendor_views.update_product_qty, name='update_product_qty'),
    path('vendor/delete-product/<int:prod_id>/', vendor_views.delete_product, name='delete_product'),
    path('contact/', vendor_views.vendor_contact, name='vendor_contact'),
    path('vendor/change-password/', vendor_views.vendor_change_password, name='vendor_change_password'),
    path('vendor/forgot-password/', vendor_views.vendor_forgot_password, name='vendor_forgot_password_url'),
    path('vendor/reset-password/', vendor_views.vendor_reset_password, name='vendor_reset_password_url'),
    path('vendor/request-removal/', vendor_views.vendor_request_removal, name='vendor_request_removal'),
    path('check_vendor_status/', vendor_views.check_vendor_status, name='check_vendor_status'),

]