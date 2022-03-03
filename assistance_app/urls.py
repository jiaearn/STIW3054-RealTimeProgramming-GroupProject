from django.urls import path
from . import views

urlpatterns = [
    path('requestassistance/<int:id>', views.request_assistance, name="request_assistance"),
    path("applicationrecord/<int:id>", views.list_assistance_type, name='list_assistance_type'),
    # path("edit/<id>", views.edit_assistance_type, name='edit_assistance_type'),
]