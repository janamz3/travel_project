from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('add/', views.add_trip, name='add_trip'),
    path('trip/<int:pk>/edit/', views.edit_trip, name='edit_trip'),
    path('trip/<int:pk>/delete/', views.delete_trip, name='delete_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]