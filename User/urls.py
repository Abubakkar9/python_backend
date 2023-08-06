
from django.urls import path
from User import views 

urlpatterns = [
    path('users/', views.Users.as_view(), name="users"),
    
]