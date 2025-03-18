from django import forms
from django.forms import inlineformset_factory
from store.models import Product,ProductAttribute

class NewProductForm(forms.ModelForm):
	class Meta:
		model=Product
		fields=('category','subcategory','festival','season','name','description','price','image','image_1', 'image_2','image_3',     
            'image_4', )   

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('attribute_name', 'attribute_value')
        widgets = {
            'attribute_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attribute Name'}),
            'attribute_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attribute Value'}),
        }

# Formset for Custom Attributes
ProductAttributeFormSet = inlineformset_factory(
    Product,
    ProductAttribute,
    form=ProductAttributeForm,
    extra=1,
    can_delete=True,
)
