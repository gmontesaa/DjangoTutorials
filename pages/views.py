
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect

# Create your views here.

#def homePageView(request): # new
  #  return HttpResponse('Hello World!') # new

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Geronimo Montes",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "contact@example.com",
            "address": "123 Fake Street, Medellín, Colombia",
            "phone": "+57 300 123 4567",
        })
        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1000},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1200},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 50},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 100}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        context = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, context)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return redirect('home')

        context = {
            "title": product["name"] + " - Online Store",
            "subtitle": product["name"] + " - Product information",
            "product": product
        }
        return render(request, self.template_name, context)

class ProductCreateView(View):
    template_name = 'products/create.html'
    success_template_name = 'products/success.html'

    def get(self, request):
        form = ProductForm()
        context = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Aquí podrías guardar el producto (si tuvieras base de datos)
            return render(request, self.success_template_name)
        else:
            context = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, context)
