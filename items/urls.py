from django.urls import path
from . import views

urlpatterns = [
    path('', views.userLogin, name='login'),
    path('login', views.userLogin, name='login'),
    path('logout', views.userLogout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('items', views.items, name='items'),
    path('addItem', views.addItem, name='addItem'),
    path('summary', views.summary, name='summary'),
    path('editItem/<str:pk>', views.editItem, name='editItem'),
    path('deleteItem/<str:pk>', views.deleteItem, name='deleteItem'),
]