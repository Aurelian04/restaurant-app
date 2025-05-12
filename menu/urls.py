from django.urls import path
from menu import views


app_name = 'menu'

urlpatterns = [
    path("create", views.MenuView.as_view(), name='create-item'),
    path("update/<int:pk>/", views.UpdateMenuItemView.as_view(), name='update-item'),
    path("", views.PublicMenuView.as_view(), name="public-menu"),
]