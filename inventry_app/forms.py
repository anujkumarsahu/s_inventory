from django import forms
from . models import *


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'contact_no']



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','item_code', 'price']
     


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['invoice','supplier', 'datetime']
        widgets = {
            'datetime': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }
    
    
class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetails
        fields=['item','quantity','price','amount']
    widgets = {
        'quantity': forms.NumberInput(attrs={'class': 'mr-md-4'}),
        'price': forms.NumberInput(attrs={'class': 'mr-md-4'}),
        'amount': forms.NumberInput(attrs={'class': 'mr-md-4'}),
        
        'item': forms.Select(attrs={'class': 'mr-md-4'}),
    }
    quantity = forms.IntegerField(widget=widgets['quantity'])
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=widgets['price'])
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=widgets['amount'])
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=widgets['item'])

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer','contact_no']


class SaleDetailForm(forms.ModelForm):
    class Meta:
        model= SaleDetail
        fields=['item','quantity','price','amount']

 
class PurchaseReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'mr-md-4 ', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'mr-md-4 ', 'type': 'date'}))


class SaleReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'mr-md-4 ', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'mr-md-4 ', 'type': 'date'}))


