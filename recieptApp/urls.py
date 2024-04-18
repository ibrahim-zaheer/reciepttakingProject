from django.urls import path
from . import views
urlpatterns = [
  # URL pattern for displaying receipts
    path('receipts/', views.receipts, name='receipts'),
path('receipts/<int:id>/update/', views.update_receipt, name='update_receipt'),
path('receipts/<int:id>/delete/', views.delete_receipt, name='delete_receipt'),


    # URL pattern for the user login page
    path('login/', views.login_page, name='login'),

    # URL pattern for the user registration page
    path('register/', views.register_page, name='register'),
    path('', views.register_page, name='register'),

    # URL pattern for user logout
    path('logout/', views.custom_logout, name='logout'),

    # URL pattern for generating PDF receipts
    path('pdf/', views.pdf, name='pdf'),   
]
