from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('login/', views.log_in, name='log'),
    path('register/', views.register, name='register'),
    path("", views.MyView.as_view(), name='home'),
    path('rooms/', views.room_view, name='room_list'),
    path('rooms/<int:pk>/', views.book_room, name='book_room'),
    path('facilities/', views.Facilities.as_view(), name='facilities'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('booking/', booking_view, name='booking_view'),
    # path('room/create/', room_create, name='room_create'),
    path('booking/detail/', booking_detail, name='booking_detail'),
]
