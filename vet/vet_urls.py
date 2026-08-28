from django.urls import path
from . import vet_views

urlpatterns = [
    path('register/', vet_views.vet_register, name='vet_register'),
    path('login/', vet_views.vet_login, name='vet_login'),
    path('vet_dashboard/',vet_views.vet_dashboard,name="vet_dashboard"),
    path('request_removal/', vet_views.request_removal, name='request_removal'),
    path('check-vet-status/', vet_views.check_vet_status, name='check_vet_status'),
    path('vet-logout/', vet_views.vet_logout, name='vet_logout'),
    path('forgot-password/', vet_views.vet_forgot_password, name='vet_forgot_password_url'),
    path('reset-password/', vet_views.vet_reset_password, name='vet_reset_password_url'),
    path('update-schedule/', vet_views.update_vet_schedule, name='update_vet_schedule'),
    path('vet/change-password/', vet_views.vet_change_password, name='vet_change_password'),
    path('vet_contact/',vet_views.vet_contact,name='vet_contact'),
]