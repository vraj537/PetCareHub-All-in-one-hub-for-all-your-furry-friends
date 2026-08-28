from django.shortcuts import redirect
from django.urls import reverse, resolve

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Current URL ko resolve karein taaki pata chale view kis app ka hai
        try:
            resolver_match = resolve(request.path_info)
            # View function kis module (app) se aa raha hai wo check karein
            view_module = resolver_match._func_path
        except:
            view_module = ""

        # 2. Allowed URLs (Bina login ke admin app mein inki permission hai)
        # Taki login page par loop na bane
        allowed_urls = [
            reverse('login'),
            reverse('forgotpass'), 
            reverse('resetpass')
        ]

        # 3. Logic: Check karein agar request 'test2' (Admin) app ke liye hai
        # Hum check kar rahe hain ki kya view_module mein 'test2' naam aa raha hai
        if 'test2' in view_module:
            
            # Agar user login nahi hai aur kisi aise page par hai jo allowed list mein nahi hai
            if not request.session.get('admin_id') and request.path not in allowed_urls:
                # To seedha login page par bhejein
                return redirect('login')

        # Agar request 'client' app ki hai ya user logged in hai, to aage badhne dein
        response = self.get_response(request)
        return response