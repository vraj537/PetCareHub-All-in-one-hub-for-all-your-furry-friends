from django import forms
from test2.models import Area,ProductCategory,Product,Gallery,Customer

class updatearea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["area_id","area_name","pincode"]
    

class updateproductcategory(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ["category_id","category_name","description"]


class updateproduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["prod_id","category_id","vendor_id","prod_name","qty","description","price","cover_img_path"]


class updategallery(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["gallery_id","prod_id","image_path"]
        
class updatecustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["cust_id","area_id","cust_name","password","email","contact","address","is_admin","otp","otp_used"]