from django import forms
from ..models import Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = (
            'product_name',
            'product_desc',
            'product_full_desc',
            'product_price',
            'is_featured',
            'product_status'
        )

