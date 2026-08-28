from test2.models import Cart, Wishlist,Customer # Wishlist model bhi import kar lo
from django.db.models import Sum

def admin_sidebar_data(request):
    aid = request.session.get('admin_id') # Admin session ID
    admin_info = None
    
    if aid:
        try:
            admin_info = Customer.objects.get(cust_id=aid) # Admin ka sara data fetch karein
        except Customer.DoesNotExist:
            admin_info = None

    return {
        'user': admin_info # Ye 'user' variable ab pure project (header/sidebar) mein milega
    }

def cart_count(request):
    cust_id = request.session.get('cust_id')
    
    # Cart Count Logic (Jo aapke paas pehle se hai)
    cart_count_val = 0
    wishlist_count_val = 0
    
    if cust_id:
        # Cart total quantity
        cart_result = Cart.objects.filter(cust_id=cust_id, status=1).aggregate(total=Sum('quantity'))
        cart_count_val = cart_result.get('total') or 0
        
        # Wishlist total items
        wishlist_count_val = Wishlist.objects.filter(cust_id=cust_id).count()

    return {
        'cart_item_count': cart_count_val,
        'wishlist_count': wishlist_count_val # Ye naya variable header ke liye
    }