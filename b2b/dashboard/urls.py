from django.urls import path
from . import views

app_name='dashboard'

urlpatterns=[
    path('',views.index,name='index'),
    path('dashboard_add_product/', views.dashboard_add_product, name='dashboard_add_product'),

]