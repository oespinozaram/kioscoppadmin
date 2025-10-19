from rest_framework import viewsets, permissions
import tempfile
import os
import sqlite3
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from .models import (
    Categoria, TipoPan, TipoRelleno, TipoForma, TipoCobertura, PastelConfigurado, TipoTamano, TipoColores,
    CategoriaTiposCoberturaDisponibles,
    CategoriaTiposFormaDisponibles,
    CategoriaTiposPanDisponibles,
    CategoriaTiposRellenoDisponibles,
    CategoriaTiposCoberturaColores)
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
    CategoriaTiposCoberturaColoresSerializer,
    CategoriaSyncSerializer, PastelConfiguradoSyncSerializer
)
from dateutil.parser import parse, ParserError
from django.http import HttpResponse
from rest_framework.views import APIView


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


class DownloadDbView(APIView):
    """
    Este endpoint genera una base de datos SQLite al momento con los datos
    del catálogo y la sirve como un archivo para descargar.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Usamos un archivo temporal para construir la base de datos
        with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as tmp_db:
            db_path = tmp_db.name

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # --- 1. Crear las tablas ---
            # Aquí replicamos la estructura de los modelos de Django.
            # Nota: Los tipos de datos deben ser compatibles con SQLite (TEXT, INTEGER, REAL, BLOB, NULL).

            # Ejemplo para la tabla Categoria
            cursor.execute('''
                           CREATE TABLE categoria
                           (
                               id                   INTEGER PRIMARY KEY,
                               nombre_categoria     TEXT,
                               descripcion_pan_base TEXT,
                               imagen_quiosco       TEXT,
                               fecha_modificacion   TEXT
                           )
                           ''')

            # Ejemplo para la tabla PastelConfigurado
            cursor.execute('''
                           CREATE TABLE pastel_configurado
                           (
                               id                          INTEGER PRIMARY KEY,
                               categoria_id                INTEGER,
                               tipo_pan_seleccionado_id    INTEGER,
                               tipo_forma_seleccionada_id  INTEGER,
                               tipo_tamano_seleccionado_id INTEGER,
                               precio_base                 REAL,
                               precio_chocolate            REAL,
                               monto_deposito              REAL,
                               incluye                     TEXT,
                               peso_pastel                 TEXT,
                               medidas_pastel              TEXT,
                               fecha_modificacion          TEXT
                           )
                           ''')

            # --- AGREGAR AQUÍ los CREATE TABLE para el resto de tus modelos (TipoPan, TipoForma, etc.) ---

            # --- 2. Extraer y poblar los datos ---

            # Poblando la tabla Categoria
            categorias = Categoria.objects.all()
            for cat in categorias:
                cursor.execute(
                    "INSERT INTO categoria (id, nombre_categoria, descripcion_pan_base, imagen_quiosco, fecha_modificacion) VALUES (?, ?, ?, ?, ?)",
                    (cat.id, cat.nombre_categoria, cat.descripcion_pan_base, str(cat.imagen_quiosco),
                     str(cat.fecha_modificacion))
                )

            # Poblando la tabla PastelConfigurado
            pasteles = PastelConfigurado.objects.all()
            for p in pasteles:
                cursor.execute(
                    """INSERT INTO pastel_configurado (id, categoria_id, tipo_pan_seleccionado_id,
                                                       tipo_forma_seleccionada_id, tipo_tamano_seleccionado_id,
                                                       precio_base, precio_chocolate, monto_deposito, incluye,
                                                       peso_pastel, medidas_pastel, fecha_modificacion)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (p.id, p.categoria_id, p.tipo_pan_seleccionado_id, p.tipo_forma_seleccionada_id,
                     p.tipo_tamano_seleccionado_id, p.precio_base, p.precio_chocolate,
                     p.monto_deposito, p.incluye, p.peso_pastel, p.medidas_pastel, str(p.fecha_modificacion))
                )

            # --- AGREGAR AQUÍ la lógica para poblar el resto de tus tablas ---

            conn.commit()
            conn.close()

            # --- 3. Servir el archivo para descarga ---
            with open(db_path, 'rb') as db_file:
                response = HttpResponse(db_file.read(), content_type='application/x-sqlite3')
                response['Content-Disposition'] = 'attachment; filename="kiosco_data.sqlite3"'
                return response

        finally:
            # Asegurarse de que el archivo temporal se elimine después de servirlo
            if os.path.exists(db_path):
                os.remove(db_path)

