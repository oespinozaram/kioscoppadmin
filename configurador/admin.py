from django.contrib import admin
from .models import (
    Categoria,
    TipoPan,
    TipoForma,
    TipoRelleno,
    TipoCobertura,
    PastelConfigurado,
    TipoTamano,
    TiposDecoracion,
    TipoColores,
    CategoriaTiposCoberturaDisponibles,
    CategoriaTiposFormaDisponibles,
    CategoriaTiposPanDisponibles,
    CategoriaTiposRellenoDisponibles,
    CategoriaTiposCoberturaColores,
    CategoriaTiposCoberturaDecorados,
    DiasFestivos,
    HorarioEntrega,
    Extra
)
from django.contrib.auth.models import Group

admin.site.site_header = "KioscoPP Administration"
admin.site.site_title = "KioscoPP Administration"
admin.site.index_title = "KioscoPP Administration"

admin.site.unregister(Group)


@admin.register(TipoPan)
class TipoPanAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_pan',)
    search_fields = ('nombre_tipo_pan',)


@admin.register(TipoRelleno)
class TipoRellenoAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_relleno',)
    search_fields = ('nombre_tipo_relleno',)


@admin.register(TipoForma)
class TipoFormaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_forma', 'detalle_forma')
    search_fields = ('nombre_tipo_forma',)


@admin.register(TipoCobertura)
class TipoCoberturaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_cobertura',)
    search_fields = ('nombre_tipo_cobertura',)


@admin.register(TipoTamano)
class TipoTamanoAdmin(admin.ModelAdmin):
    list_display = ('nombre_tamano', 'descripcion')
    search_fields = ('nombre_tamano', 'descripcion')


@admin.register(TiposDecoracion)
class TiposDecoracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_decoracion',)
    search_fields = ('nombre_tipo_decoracion',)

@admin.register(TipoColores)
class TipoColoresAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo_color',)
    search_fields = ('nombre_tipo_color',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria', 'descripcion_pan_base')
    search_fields = ('nombre_categoria',)


@admin.register(PastelConfigurado)
class PastelConfiguradoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'categoria', 'tipo_pan_seleccionado',
        'tipo_forma_seleccionada',
        'tipo_tamano_seleccionado',
        'precio_base',
        'precio_chocolate',
        'monto_deposito',
        'peso_pastel',
        'medidas_pastel',
        'incluye',
    )
    list_filter = (
       'categoria', 'tipo_pan_seleccionado', 'tipo_forma_seleccionada', 'tipo_tamano_seleccionado'
    )
    search_fields = ('id', 'categoria__nombre_categoria')
    raw_id_fields = (
        'categoria', 'tipo_pan_seleccionado', 'tipo_forma_seleccionada', 'tipo_tamano_seleccionado'
    )

@admin.register(CategoriaTiposFormaDisponibles)
class CategoriaTiposFormaDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_forma')


@admin.register(CategoriaTiposRellenoDisponibles)
class CategoriaRellenoDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_pan', 'tipo_relleno')


@admin.register(CategoriaTiposCoberturaDisponibles)
class CategoriaTiposCoberturaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_pan', 'tipo_cobertura')

@admin.register(CategoriaTiposPanDisponibles)
class CategoriaPanDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_pan')


@admin.register(CategoriaTiposCoberturaColores)
class CategoriaTiposCoberturaColoresAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_cobertura', 'tipo_color')


@admin.register(CategoriaTiposCoberturaDecorados)
class CategoriaTiposCoberturaDecoradosAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tipo_cobertura', 'tipo_decorado')

admin.site.register(DiasFestivos)
admin.site.register(HorarioEntrega)
admin.site.register(Extra)
