from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from .models import (
    Categoria, TipoPan, TipoRelleno, TipoForma, TipoCobertura, PastelConfigurado, TipoTamano, TipoColores,
    CategoriaTiposCoberturaDisponibles,
    CategoriaTiposFormaDisponibles,
    CategoriaTiposPanDisponibles,
    CategoriaTiposRellenoDisponibles,
    CategoriaTiposTamanoDisponibles, CategoriaTiposCoberturaColores)
from .serializers import (
    CategoriaSerializer,
    TipoPanSerializer,
    TipoRellenoSerializer,
    TipoTamanoSerializer,
    TipoFormaSerializer,
    TipoCoberturaSerializer,
    TiposColoresSerializer,
    PastelConfiguradoSerializer,
    CategoriaTiposCoberturaDisponiblesSerializer,
    CategoriaTiposFormaDisponiblesSerializer,
    CategoriaTiposPanDisponiblesSerializer,
    CategoriaTiposRellenoDisponiblesSerializer,
    CategoriaTiposTamanoDisponiblesSerializer,
    CategoriaTiposCoberturaColoresSerializer,
    CategoriaSyncSerializer, PastelConfiguradoSyncSerializer
)
from dateutil.parser import parse, ParserError

DEFAULT_PERMISSION_CLASSES = [permissions.IsAuthenticatedOrReadOnly]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoTamanoViewSet(viewsets.ModelViewSet):
    queryset = TipoTamano.objects.all()
    serializer_class = TipoTamanoSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoPanViewSet(viewsets.ModelViewSet):
    queryset = TipoPan.objects.all()
    serializer_class = TipoPanSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoRellenoViewSet(viewsets.ModelViewSet):
    queryset = TipoRelleno.objects.all()
    serializer_class = TipoRellenoSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoFormaViewSet(viewsets.ModelViewSet):
    queryset = TipoForma.objects.all()
    serializer_class = TipoFormaSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoCoberturaViewSet(viewsets.ModelViewSet):
    queryset = TipoCobertura.objects.all()
    serializer_class = TipoCoberturaSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class TipoColoresViewSet(viewsets.ModelViewSet):
    queryset = TipoColores.objects.all()
    serializer_class = TiposColoresSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class PastelConfiguradoViewSet(viewsets.ModelViewSet):
    queryset = PastelConfigurado.objects.select_related(
        'categoria', 'tipo_pan_seleccionado', 'tipo_forma_seleccionada',
        'tipo_tamano_seleccionado' # <-- AÑADIDO
    ).all()
    serializer_class = PastelConfiguradoSerializer
    permission_classes = DEFAULT_PERMISSION_CLASSES


class CategoriaTiposCoberturaDisponiblesViewSet(viewsets.ModelViewSet):
    """
    API endpoint para las coberturas disponibles por categoría y tipo de pan.
    """
    queryset = CategoriaTiposCoberturaDisponibles.objects.all()
    serializer_class = CategoriaTiposCoberturaDisponiblesSerializer

class CategoriaTiposFormaDisponiblesViewSet(viewsets.ModelViewSet):
    """
    API endpoint para las formas disponibles por categoría.
    """
    queryset = CategoriaTiposFormaDisponibles.objects.all()
    serializer_class = CategoriaTiposFormaDisponiblesSerializer

class CategoriaTiposPanDisponiblesViewSet(viewsets.ModelViewSet):
    """
    API endpoint para los tipos de pan disponibles por categoría.
    """
    queryset = CategoriaTiposPanDisponibles.objects.all()
    serializer_class = CategoriaTiposPanDisponiblesSerializer

class CategoriaTiposRellenoDisponiblesViewSet(viewsets.ModelViewSet):
    """
    API endpoint para los rellenos disponibles por categoría y tipo de pan.
    """
    queryset = CategoriaTiposRellenoDisponibles.objects.all()
    serializer_class = CategoriaTiposRellenoDisponiblesSerializer

class CategoriaTiposTamanoDisponiblesViewSet(viewsets.ModelViewSet):
    """
    API endpoint para los tamaños disponibles por categoría.
    """
    queryset = CategoriaTiposTamanoDisponibles.objects.all()
    serializer_class = CategoriaTiposTamanoDisponiblesSerializer


class SyncView(APIView):
    def get(self, request, *args, **kwargs):
        last_sync_str = request.query_params.get('last_sync', None)

        # Querysets base
        categorias_qs = Categoria.objects.all()
        pasteles_qs = PastelConfigurado.objects.all()

        if last_sync_str:
            try:
                # Convierte el string de la URL a un objeto datetime
                last_sync_dt = parse(last_sync_str)
                # Filtra solo los registros modificados después de la última sincronización
                categorias_qs = categorias_qs.filter(fecha_modificacion__gt=last_sync_dt)
                pasteles_qs = pasteles_qs.filter(fecha_modificacion__gt=last_sync_dt)
            except (ParserError, TypeError):
                return Response(
                    {"error": "Formato de fecha inválido para 'last_sync'. Use ISO 8601."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        categoria_serializer = CategoriaSyncSerializer(categorias_qs, many=True)
        pastel_serializer = PastelConfiguradoSyncSerializer(pasteles_qs, many=True)

        response_data = {
            "categorias": categoria_serializer.data,
            "pasteles_configurados": pastel_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data

        # Extraer los datos para cada parte de la sincronización
        categorias_data = data.get('categorias', [])
        pasteles_data = data.get('pasteles_configurados', [])

        # Validar y guardar las categorías
        categoria_serializer = CategoriaSyncSerializer(data=categorias_data, many=True)
        if categoria_serializer.is_valid():
            categoria_serializer.save()
        else:
            return Response(categoria_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validar y guardar los pasteles configurados
        pastel_serializer = PastelConfiguradoSyncSerializer(data=pasteles_data, many=True)
        if pastel_serializer.is_valid():
            pastel_serializer.save()
        else:
            return Response(pastel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Sincronización completada exitosamente"},
            status=status.HTTP_200_OK
        )