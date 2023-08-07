
from django.urls import path
from User import views 

urlpatterns = [
    path('api/users/', views.Users.as_view(), name="users"),
    path('api/users/<int:id>/', views.Users.as_view(), name="users_update_delete")
]
