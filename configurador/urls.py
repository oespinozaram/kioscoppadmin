from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    TipoPanViewSet,
    TipoRellenoViewSet,
    TipoTamanoViewSet,
    TipoFormaViewSet,
    TipoCoberturaViewSet,
    TipoColoresViewSet,
    PastelConfiguradoViewSet,
    CategoriaTiposCoberturaDisponiblesViewSet,
    CategoriaTiposFormaDisponiblesViewSet,
    CategoriaTiposPanDisponiblesViewSet,
    CategoriaTiposRellenoDisponiblesViewSet,
    CategoriaTiposTamanoDisponiblesViewSet,
    SyncView
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'tipos-pan', TipoPanViewSet, basename='tipopan')
router.register(r'tipos-relleno', TipoRellenoViewSet, basename='tiporelleno')
router.register(r'tipos-forma', TipoFormaViewSet, basename='tipoforma')
router.register(r'tipos-cobertura', TipoCoberturaViewSet, basename='tipocobertura')
router.register(r'tipos-tamano', TipoTamanoViewSet, basename='tipotamano')
router.register(r'colores', TipoColoresViewSet, basename='colores')
router.register(r'pasteles-configurados', PastelConfiguradoViewSet, basename='pastelconfigurado')
router.register(
    r'coberturas-disponibles',
    CategoriaTiposCoberturaDisponiblesViewSet,
    basename='coberturas-disponibles'
)
router.register(
    r'formas-disponibles',
    CategoriaTiposFormaDisponiblesViewSet,
    basename='formas-disponibles'
)
router.register(
    r'panes-disponibles',
    CategoriaTiposPanDisponiblesViewSet,
    basename='panes-disponibles'
)
router.register(
    r'rellenos-disponibles',
    CategoriaTiposRellenoDisponiblesViewSet,
    basename='rellenos-disponibles'
)
router.register(
    r'tamanos-disponibles',
    CategoriaTiposTamanoDisponiblesViewSet,
    basename='tamanos-disponibles'
)

urlpatterns = [
    path('', include(router.urls)),
    #path('sync', SyncView.as_view(), name='sync'),
]
