from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cliente/<int:cliente_id>/', views.cliente_topicos, name='cliente_topicos'),
    path('topico/<int:topico_id>/', views.topico_detalhe, name='topico_detalhe'),
    path('cliente/<int:cliente_id>/criar/', views.topico_criar, name='topico_criar'),
    path('topico/<int:topico_id>/editar/', views.topico_editar, name='topico_editar'),
]