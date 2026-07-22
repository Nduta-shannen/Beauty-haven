from django. urls import path
from.import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path ('', views.home, name='home'),
    path ('shop/', views.shop, name='shop'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<int:pk>/', views.category, name='category'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact,name='contact'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path("wishlist/add/<int:pk>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
