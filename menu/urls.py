from django.urls import path
from menu import views


app_name = 'menu'

urlpatterns = [
    path('', views.MenuView.as_view(), name='create'),
    path("update/<int:pk>/", views.UpdateMenuItemView.as_view(), name='update'),
]