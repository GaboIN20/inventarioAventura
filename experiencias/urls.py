from django.urls import path
from . import views

urlpatterns = [
    # Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    # Experiencias
    path('gestion/', views.lista_experiencias, name='lista_experiencias'),
    path('gestion/nueva/', views.crear_experiencia, name='crear_experiencia'),
    path('gestion/editar/<int:id>/', views.editar_experiencia, name='editar_experiencia'),
    path('gestion/eliminar/<int:id>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    # Catálogo y Reservas
    path('catalogo/', views.catalogo_turista, name='catalogo'),
    path('inscribir/<int:id>/', views.inscribir_experiencia, name='inscribir_experiencia'),
    path('reservas/', views.mis_reservas, name='mis_reservas'),
    path('reservas/confirmar/<int:id>/', views.confirmar_pago, name='confirmar_pago'),
]