from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('product-comparison/', views.ProductComparisonView.as_view(), name='product_comparison'),
    path('my-wishlist/', views.MyWishlistView.as_view(), name='my_wishlist'),
    path('terms-conditions/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('compare/add/<int:product_id>/', views.AddToCompareView.as_view(), name='add_to_compare'),
    path('compare/remove/<int:product_id>/', views.RemoveFromCompareView.as_view(), name='remove_from_compare'),
]