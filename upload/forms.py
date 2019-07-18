from django import forms
from .models import Category, Settings, Products
from django.forms import ValidationError



class CategoryForm(forms.ModelForm):
    class Meta:
         model = Category
         fields = '__all__'

class SettingsForm(forms.Form):
    ending_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    min_comp_price = forms.IntegerField(max_value=100, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    max_comp_price = forms.IntegerField(max_value=100, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    min_price = forms.IntegerField(max_value=1000, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    max_price = forms.IntegerField(max_value=1000, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    min_margin = forms.IntegerField(max_value=1000, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    max_margin = forms.IntegerField(max_value=1000, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    min_volume = forms.IntegerField(max_value=100, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    max_volume = forms.IntegerField(max_value=100, required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))

store = Products.objects.order_by('StoreId').values_list('StoreId', flat=True).distinct()

class SearchForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    upc = forms.CharField(label='UPC', max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(),required=False)
    store_id = forms.CharField(label="Store Id", widget=forms.TextInput(),required=True)
    sub_department = forms.CharField(label="Sub Department ", widget=forms.TextInput(),required=False)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        store_id = cleaned_data.get("store_id")

        if store_id=="STORE ID":
            raise ValidationError("StoreId Required")

class PromoSearchForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    upc = forms.CharField(label='UPC', max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(),required=False)
    store_id = forms.CharField(label="Store Id", widget=forms.TextInput(),required=True)
    sub_department = forms.CharField(label="Sub Department ", widget=forms.TextInput(),required=False)
    promotype = forms.CharField(label='Promotion Type', max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    promotionname = forms.CharField(label='Promotion Name', max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    startdate = forms.CharField(label="Start Date", widget=forms.TextInput(attrs={"class": "form-control"}),required=True)
    enddate = forms.CharField(label="End Date", widget=forms.TextInput(attrs={"class": "form-control"}),required=True)
    nb1_newprice = forms.CharField(label="NB1 New Price", required=False)

# class NewPriceForm(forms.Form):
#     nb_newprice = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))


class ExecutionSearchForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=250, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    upc = forms.CharField(label='UPC', max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(label="Category", widget=forms.TextInput(),required=False)
    store_id = forms.CharField(label="Store Id", widget=forms.TextInput(),required=False)
    sub_department = forms.CharField(label="Sub Department ", widget=forms.TextInput(),required=False)
