

from django.urls import path


from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('product/<int:pk>/', views.product, name='product'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update-info/', views.update_info, name='update_info'),  # Ensure the path is correct
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('filter_dropdown/', views.filter_dropdown, name='filter_dropdown'),
    path('category/<int:category_id>/', views.catfilter, name='catfilter'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_view, name='subcategory_view'),
    path('search1',views.search, name='search1'),
    path('city/<int:city_id>/', views.cityfilter, name='cityfilter'),
    path('products/filter/<int:location>/<int:category_id>/', views.product_filter, name='products_filter'),
    path('products/filter/<int:location>/<int:category_id>/<int:subcategory_id>/', views.product_filter, name='products_filter_by_subcategory'),
    path('enquiry/', views.send_enquiry, name='send_enquiry'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/',views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('best-price/', views.best_price, name='best_price'),
    path('view-categories/', views.view_categories, name='view_categories'),
    path('sort/<str:sv>/', views.sort, name='sort'),
    path('filterbyprice',views.filterbyprice),
    path('seller_req/',views.seller_req, name='seller_req'),
    

]
