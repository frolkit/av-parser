from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('add/', views.add, name='create_item'),
    path('stat/', views.stat, name='stat_item'),
    path('top/', views.top, name='top_item'),
    path('redoc/',
         TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
]
