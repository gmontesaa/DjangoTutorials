from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    ContactPageView,
    ProductIndexView,
    ProductShowView,
    ProductCreateView,
    ProductListView,
    CartView,
    CartRemoveAllView,
    ImageView,
    ImageViewNoDI,  # ✅ Importamos ImageViewNoDI
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("products/", ProductIndexView.as_view(), name="products_index"),
    path("products/<int:id>/", ProductShowView.as_view(), name="product_show"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("product-list/", ProductListView.as_view(), name="product_list"),
    path("cart/", CartView.as_view(), name="cart_index"),
    path("cart/remove_all/", CartRemoveAllView.as_view(), name="cart_remove_all"),
    # Vistas de imagen
    path("image/", ImageView.as_view(), name="image_index"),
    path("image/<str:image_name>/", ImageView.as_view(), name="image_view"),
    path("image/upload/", ImageView.as_view(), name="image_upload"),
    # ✅ Nuevas rutas para ImageViewNoDI
    path("imagenotdi/", ImageViewNoDI.as_view(), name="imagenodi_index"),
    path("image/save", ImageViewNoDI.as_view(), name="imagenodi_save"),
]
