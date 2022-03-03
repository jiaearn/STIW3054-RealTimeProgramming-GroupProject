from django.urls import path
from . import views

urlpatterns = [
    path('listvictim/', views.list_victim, name="list_victim"),
    path("listvictim/<int:id>/assistance/", views.view_victim_assistance, name="view_victim_assistance"),
    path("listvictim/<int:id>/assistance/delete", views.delete_victim_assistance, name="delete_victim_assistance"),
    path("listvictim/<int:victim_id>/assistance/<int:assistance_id>/edit", views.edit_victim_assistance, name="edit_victim_assistance"),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('addvictim/', views.add_victim, name="add_victim"),
    path('editvictim/<int:id>', views.edit_victim, name="edit_victim"),
    path('deletevictim/<int:id>', views.delete_victim, name="delete_victim"),
]