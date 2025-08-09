from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
import os
from django.conf import settings


# --------------------------
# Formulario de productos
# --------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


# --------------------------
# Vistas de páginas estáticas
# --------------------------
class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Geronimo Montes",
            }
        )
        return context


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Contact - Online Store",
                "subtitle": "Contact Us",
                "email": "contact@example.com",
                "address": "123 Fake Street, Medellín, Colombia",
                "phone": "+57 300 123 4567",
            }
        )
        return context


# --------------------------
# Vistas de productos
# --------------------------
class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all(),
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return redirect("home")

        viewData = {
            "title": product.name + " - Online Store",
            "subtitle": product.name + " - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


class ProductCreateView(View):
    template_name = "products/create.html"
    success_template_name = "products/success.html"

    def get(self, request):
        form = ProductForm()
        context = {"title": "Create product", "form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.success_template_name)
        else:
            context = {"title": "Create product", "form": form}
            return render(request, self.template_name, context)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context


# --------------------------
# Vistas del carrito
# --------------------------
class CartView(View):
    template_name = "cart/index.html"

    def get(self, request):
        products = {
            121: {"name": "Tv samsung", "price": "1000"},
            11: {"name": "Iphone", "price": "2000"},
        }

        cart_products = {}
        cart_product_data = request.session.get("cart_product_data", {})
        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        view_data = {
            "title": "Cart - Online Store",
            "subtitle": "Shopping Cart",
            "products": products,
            "cart_products": cart_products,
        }
        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        cart_product_data = request


class CartRemoveAllView(View):
    def post(self, request):
        request.session["cart_product_data"] = {}
        request.session.modified = True
        return redirect("cart_index")


# --------------------------
# Vista de imágenes
# --------------------------
class ImageView(View):
    def get(self, request):
        return render(request, "images/index.html")  # ✅ corregido, sin 'templates/'

    def post(self, request):
        uploaded_file = request.FILES.get("profile_image")
        image_url = None

        if uploaded_file:
            save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(save_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            image_url = settings.MEDIA_URL + uploaded_file.name

        return render(request, "images/index.html", {"image_url": image_url})


class ImageViewNoDI(View):
    template_name = "images/index.html"

    def get(self, request):
        image_url = request.session.get("image_url", "")
        return render(request, self.template_name, {"image_url": image_url})

    def post(self, request):
        uploaded_file = request.FILES.get("profile_image")
        image_url = None

        if uploaded_file:
            save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(save_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            image_url = settings.MEDIA_URL + uploaded_file.name

        request.session["image_url"] = image_url
        return redirect("imagenodi_index")
