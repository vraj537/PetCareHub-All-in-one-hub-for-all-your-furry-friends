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
from django.contrib import admin
from django.urls import path,include
from test2 import views


from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('tables/',views.show),
    path('login/',views.login,name='login'),
    path('forgotpass/',views.forgotpass,name='forgotpass'),
    path('resetpass/',views.resetpassword,name='resetpass'),
    path('area_table/',views.area_table,name='area_table'),
    path('customer_table/',views.customer_table,name='customer_table'),
    path('vet_table/',views.vet_table,name='vet_table'),
    path('update-status/<int:v_id>/<str:action>/', views.update_vet_status, name='update_vet_status'),
    path('vendor_table/',views.vendor_table,name='vendor_table'),
    path('update_vendor_status/<int:v_id>/<str:action>/', views.update_vendor_status, name='update_vendor_status'),
    path('delete-vendor/<int:v_id>/', views.delete_vendor, name='delete_vendor'),
    path('deliveryboy_table/',views.deliveryboy_table,name='deliveryboy_table'),
    path('appointment_table/',views.appointment_table,name='appointment_table'),
    path('productcategory_table/',views.productcategory_table,name='productcategory_table'),
    path('product_table/',views.product_table,name='product_table'),
    path('order_table/',views.order_table,name='order_table'),
    path('orderdetail_table/',views.orderdetail_table,name='orderdetail_table'),
    path('appointmentpayment_table/',views.appointmentpayment_table,name='appointmentpayment_table'),
    path('orderpayment_table/',views.orderpayment_table,name='orderpayment_table'),
    path('feedback_table/',views.feedback_table,name='feedback_table'),
    path('gallery_table/',views.gallery_table,name='gallery_table'),
    path('wishlist_table/',views.wishlist_table,name='wishlist_table'),
    path('cart_table/',views.cart_table,name='cart_table'),
    path('update_area_table/<int:id>',views.update_area_table,name='update_area_table'),
    path('area_delete/<int:id>',views.area_delete,name='area_delete'),
    path('update_productcategory_table/<int:id>',views.update_productcategory_table,name='update_productcategory_table'),
    path('productcategory_delete/<int:id>',views.productcategory_delete),
    path('update_product_table/<int:id>',views.update_product_table,name='update_product_table'),
    path('product_delete/<int:id>',views.product_delete),
    path('update_gallery_table/<int:id>',views.update_gallery_table,name='update_gallery_table'),
    path('gallery_delete/<int:id>',views.gallery_delete),
    path('insert_area_table/',views.insert_area_table,name='insert_area_table'),
    path('insert_productcategory_table/',views.insert_productcategory_table),
    path('insert_product_table/',views.insert_product_table),
    path('insert_gallery_table/',views.insert_gallery_table),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('vet-schedule/', views.vet_schedule_table, name='vet_schedule_table'),
    path('profile/',views.profile,name="profile"),
    path('logout/', views.logout, name='logout'),
    path('update_vet_status/<int:v_id>/<str:action>/', views.update_vet_status, name='update_vet_status'),
    path('delete_vet/<int:v_id>/', views.delete_vet, name='delete_vet'),
    path('update-customer/<int:c_id>/<str:action>/', views.update_customer_status, name='update_customer_status'),
    path('client/',include('client.client_urls')),
    path('change_password/', views.change_password, name="change_password"),
    path('vet/', include('vet.vet_urls')),
    path('deliveryboy/', include('deliveryboy.deliveryboy_urls')),
    path('vendor/', include('vendor.vendor_urls')),

]

# Ye logic static aur media files serve karne ke liye hai
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
