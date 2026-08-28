from django.shortcuts import redirect
from django.urls import reverse, resolve
from test2.models import Customer
from django.contrib import messages

class ClientAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolver_match = resolve(request.path_info)
            view_module = resolver_match._func_path
        except:
            view_module = ""

        if 'client' in view_module:
            cust_id = request.session.get('cust_id')
            if cust_id:
                try:
                    customer = Customer.objects.get(cust_id=cust_id)
                    if customer.is_admin == 2:  # Restricted!
                        # Sirf client session variables hatao, flush nahi
                        request.session.pop('cust_id', None)
                        request.session.pop('cust_name', None)
                        request.session.pop('is_admin', None)
                        request.session.pop('cust_profile', None)
                        messages.error(request, "Your account has been restricted.")
                        return redirect('login1')
                except Customer.DoesNotExist:
                    request.session.pop('cust_id', None)
                    request.session.pop('cust_name', None)
                    request.session.pop('is_admin', None)
                    request.session.pop('cust_profile', None)
                    return redirect('login1')

        response = self.get_response(request)
        return response