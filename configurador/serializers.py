
from rest_framework import serializers
from .models import (
    Categoria,
    TipoPan,
    TipoRelleno,
    TipoForma,
    TipoCobertura,
    PastelConfigurado,
    TipoTamano,
    TipoColores,
    CategoriaTiposCoberturaDisponibles,
    CategoriaTiposFormaDisponibles,
    CategoriaTiposPanDisponibles,
    CategoriaTiposRellenoDisponibles,
    CategoriaTiposTamanoDisponibles,
    CategoriaTiposCoberturaColores
)


class TipoPanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPan
        fields = '__all__'


class TipoTamanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTamano
        fields = '__all__'


class TipoRellenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRelleno
        fields = '__all__'


class TipoFormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoForma
        fields = '__all__'


class TipoCoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCobertura
        fields = '__all__'


class TiposColoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoColores
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre_categoria', 'descripcion_pan_base',
            'imagen_quiosco'
        ]


class PastelConfiguradoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre_categoria', read_only=True)
    tipo_pan_seleccionado_nombre = serializers.CharField(source='tipo_pan_seleccionado.nombre_tipo_pan', read_only=True)
    tipo_forma_seleccionada_nombre = serializers.CharField(source='tipo_forma_seleccionada.nombre_tipo_forma',
                                                           read_only=True)
    tipo_tamano_seleccionado_nombre = serializers.CharField(source='tipo_tamano_seleccionado.nombre_tamano',
                                                            read_only=True)

    class Meta:
        model = PastelConfigurado
        fields = [
            'id', 'categoria', 'tipo_pan_seleccionado', 'tipo_forma_seleccionada',
            'tipo_tamano_seleccionado',
            'precio_base', 'precio_chocolate', 'monto_deposito', 'incluye', 'peso_pastel', 'medidas_pastel',
            'fecha_modificacion',
            'categoria_nombre', 'tipo_pan_seleccionado_nombre', 'tipo_forma_seleccionada_nombre',
            'tipo_tamano_seleccionado_nombre'
        ]


class CategoriaTiposCoberturaDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposCoberturaDisponibles
        # Incluimos todos los campos del modelo en la API
        fields = '__all__'

class CategoriaTiposFormaDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposFormaDisponibles
        fields = '__all__'

class CategoriaTiposPanDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposPanDisponibles
        fields = '__all__'

class CategoriaTiposRellenoDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposRellenoDisponibles
        fields = '__all__'

class CategoriaTiposTamanoDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposTamanoDisponibles
        fields = '__all__'

class CategoriaTiposCoberturaColoresSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import CategoriaTiposCoberturaColores
        model = CategoriaTiposCoberturaColores
        fields = '__all__'


class TiposPanDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposPanDisponibles
        fields = ['tipo_pan', 'imagen_quisco']


class TiposRellenoDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposRellenoDisponibles
        fields = ['tipo_pan', 'tipo_relleno', 'imagen_quisco']


class TiposCoberturaDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposCoberturaDisponibles
        fields = ['tipo_cobertura', 'tipo_pan', 'imagen_quisco']


class TiposFormaDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposFormaDisponibles
        fields = ['tipo_forma', 'imagen_quisco']


class TiposTamanoDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposTamanoDisponibles
        fields = ['tipo_tamano']


class ColoresCoberturaDisponiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTiposCoberturaColores
        fields = ['tipo_cobertura', 'tipo_color']



# Serializer principal para Categoria
class CategoriaSyncSerializer(serializers.ModelSerializer):
    # Campos anidados que aceptarán una lista de objetos
    tipos_pan_disponibles = TiposPanDisponiblesSerializer(
        source='categoriatipospandisponibles_set', many=True
    )
    tipos_relleno_disponibles = TiposRellenoDisponiblesSerializer(
        source='categoriatiposrellenodisponibles_set', many=True
    )
    tipos_cobertura_disponibles = TiposCoberturaDisponiblesSerializer(
        source='categoriatiposcoberturadisponibles_set', many=True
    )
    tipos_forma_disponibles = TiposFormaDisponiblesSerializer(
        source='categoriatiposformadisponibles_set', many=True
    )
    tipos_tamano_disponibles = TiposTamanoDisponiblesSerializer(
        source='categoriatipostamanodisponibles_set', many=True
    )
    colores_cobertura_disponibles = ColoresCoberturaDisponiblesSerializer(
        source='categoriatiposcoberturacolores_set', many=True
    )

    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre_categoria', 'descripcion_pan_base', 'imagen_quiosco',
            'tipos_pan_disponibles', 'tipos_relleno_disponibles', 'tipos_cobertura_disponibles',
            'tipos_forma_disponibles', 'tipos_tamano_disponibles', 'colores_cobertura_disponibles'
        ]

    def create(self, validated_data):
        tipos_pan_data = validated_data.pop('tipos_pan_disponibles')
        tipos_relleno_data = validated_data.pop('tipos_relleno_disponibles')
        tipos_cobertura_data = validated_data.pop('tipos_cobertura_disponibles')
        tipos_forma_data = validated_data.pop('tipos_forma_disponibles')
        tipos_tamano_data = validated_data.pop('tipos_tamano_disponibles')
        colores_cobertura_data = validated_data.pop('colores_cobertura_disponibles')

        categoria, created = Categoria.objects.update_or_create(
            id=validated_data.get('id'),
            defaults=validated_data
        )

        # Eliminar relaciones existentes por categoría
        CategoriaTiposPanDisponibles.objects.filter(categoria=categoria).delete()
        CategoriaTiposRellenoDisponibles.objects.filter(categoria=categoria).delete()
        CategoriaTiposCoberturaDisponibles.objects.filter(categoria=categoria).delete()
        CategoriaTiposFormaDisponibles.objects.filter(categoria=categoria).delete()
        CategoriaTiposTamanoDisponibles.objects.filter(categoria=categoria).delete()
        CategoriaTiposCoberturaColores.objects.filter(categoria=categoria).delete()

        # Recrear relaciones
        for item_data in tipos_pan_data:
            CategoriaTiposPanDisponibles.objects.create(categoria=categoria, **item_data)
        for item_data in tipos_relleno_data:
            CategoriaTiposRellenoDisponibles.objects.create(categoria=categoria, **item_data)
        for item_data in tipos_cobertura_data:
            CategoriaTiposCoberturaDisponibles.objects.create(categoria=categoria, **item_data)
        for item_data in tipos_forma_data:
            CategoriaTiposFormaDisponibles.objects.create(categoria=categoria, **item_data)
        for item_data in tipos_tamano_data:
            CategoriaTiposTamanoDisponibles.objects.create(categoria=categoria, **item_data)
        for item_data in colores_cobertura_data:
            CategoriaTiposCoberturaColores.objects.create(categoria=categoria, **item_data)

        return categoria


# Serializer para PastelConfigurado
class PastelConfiguradoSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastelConfigurado
        fields = '__all__'

    def create(self, validated_data):
        pastel, created = PastelConfigurado.objects.update_or_create(
            id=validated_data.get('id'),
            defaults=validated_data
        )
        return pastel
