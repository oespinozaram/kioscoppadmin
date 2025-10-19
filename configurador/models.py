from django.db import models


class TipoTamano(models.Model):
    nombre_tamano = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tamaño")
    descripcion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descripción (ej: porciones, dimensiones)")
    peso = models.CharField(max_length=50, blank=True, null=True, verbose_name="Peso")

    def __str__(self):
        return self.nombre_tamano

    class Meta:
        verbose_name = "Tipo de Tamaño"
        verbose_name_plural = "Tipos de Tamaño"
        ordering = ['nombre_tamano']


class TipoPan(models.Model):
    nombre_tipo_pan = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Pan")

    def __str__(self):
        return self.nombre_tipo_pan

    class Meta:
        verbose_name = "Tipo de Pan"
        verbose_name_plural = "Tipos de Pan"


class TipoRelleno(models.Model):
    nombre_tipo_relleno = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Tipo de Relleno")

    def __str__(self):
        return self.nombre_tipo_relleno

    class Meta:
        verbose_name = "Tipo de Relleno"
        verbose_name_plural = "Tipos de Relleno"


class TipoForma(models.Model):
    nombre_tipo_forma = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Forma")
    detalle_forma = models.CharField(max_length=255, blank=True, null=True, verbose_name="Detalle de la Forma")

    def __str__(self):
        return self.nombre_tipo_forma

    class Meta:
        verbose_name = "Tipo de Forma"
        verbose_name_plural = "Tipos de Forma"


class TipoCobertura(models.Model):
    nombre_tipo_cobertura = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Tipo de Cobertura")

    def __str__(self):
        return self.nombre_tipo_cobertura

    class Meta:
        verbose_name = "Tipo de Cobertura"
        verbose_name_plural = "Tipos de Cobertura"


class TiposDecoracion(models.Model):
    nombre_tipo_decoracion = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Tipo de Decoración")

    def __str__(self):
        return self.nombre_tipo_decoracion

    class Meta:
        verbose_name = "Tipo de Decorado"
        verbose_name_plural = "Tipos de Decorados"


class TipoColores(models.Model):
    nombre_tipo_color = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Colores")

    def __str__(self):
        return self.nombre_tipo_color

    class Meta:
        verbose_name = "Tipo de Color"
        verbose_name_plural = "Tipos de Colores"


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion_pan_base = models.CharField(max_length=255, blank=True, null=True,
                                            verbose_name="Descripción del Pan Base")
    imagen_quiosco = models.ImageField(upload_to="categorias/", blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class PastelConfigurado(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='pasteles_configurados',
                                  verbose_name="Categoría")
    tipo_pan_seleccionado = models.ForeignKey(TipoPan, on_delete=models.PROTECT, related_name='pasteles_con_este_pan',
                                              verbose_name="Pan Seleccionado")
    tipo_forma_seleccionada = models.ForeignKey(TipoForma, on_delete=models.PROTECT,
                                                related_name='pasteles_con_esta_forma',
                                                verbose_name="Forma Seleccionada")
    tipo_tamano_seleccionado = models.ForeignKey(
        TipoTamano,
        on_delete=models.PROTECT,
        related_name='pasteles_con_este_tamano',
        verbose_name="Tamaño Seleccionado"
    )


    precio_base = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name="Precio Base")
    precio_chocolate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           verbose_name="Precio Chocolate")
    monto_deposito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    incluye = models.TextField(blank=True, null=True)
    peso_pastel = models.CharField(max_length=30, null=True, blank=True)
    medidas_pastel = models.TextField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        tamano_str = self.tipo_tamano_seleccionado.nombre_tamano if self.tipo_tamano_seleccionado else "N/A"
        return f"Pastel ID-{self.id} ({self.categoria.nombre_categoria}) - Tam: {tamano_str}"

    class Meta:
        verbose_name = "Pastel Configurado"
        verbose_name_plural = "Pasteles Configurados"


class CategoriaTiposCoberturaDisponibles(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    tipo_pan = models.ForeignKey(TipoPan, on_delete=models.CASCADE, db_column='id_tipo_pan')
    tipo_cobertura = models.ForeignKey(TipoCobertura, on_delete=models.CASCADE, db_column='id_tipo_cobertura')
    imagen_quisco = models.ImageField(upload_to="coberturas/", blank=True, null=True)

    def __str__(self):
        categoria = self.categoria.nombre_categoria if self.categoria_id else ""
        tipo_pan = self.tipo_pan.nombre_tipo_pan if self.tipo_pan_id else ""
        return f"{categoria} - {tipo_pan}"

    class Meta:
        db_table = 'categoria_tipos_cobertura_disponibles'
        # Replicamos la llave primaria compuesta con unique_together`
        unique_together = ('categoria', 'tipo_pan', 'tipo_cobertura')
        verbose_name = 'Cobertura Disponible por Categoría'
        verbose_name_plural = 'Coberturas Disponibles por Categoría'


class CategoriaTiposFormaDisponibles(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    tipo_forma = models.ForeignKey(TipoForma, on_delete=models.CASCADE, db_column='id_tipo_forma')
    imagen_quisco = models.ImageField(upload_to="formas/", blank=True, null=True)

    def __str__(self):
        return f"{self.categoria} - {self.tipo_forma}"

    class Meta:
        db_table = 'categoria_tipos_forma_disponibles'
        unique_together = ('categoria', 'tipo_forma')
        verbose_name = 'Forma Disponible por Categoría'
        verbose_name_plural = 'Formas Disponibles por Categoría'


class CategoriaTiposPanDisponibles(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria', related_name='tipos_pan_disponibles')
    tipo_pan = models.ForeignKey(TipoPan, on_delete=models.CASCADE, db_column='id_tipo_pan')
    imagen_quisco = models.ImageField(upload_to="panes/", blank=True, null=True)

    def __str__(self):
        return f"{self.categoria} - {self.tipo_pan}"

    class Meta:
        db_table = 'categoria_tipos_pan_disponibles'
        unique_together = ('categoria', 'tipo_pan')
        verbose_name = 'Pan Disponible por Categoría'
        verbose_name_plural = 'Panes Disponibles por Categoría'


class CategoriaTiposRellenoDisponibles(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    tipo_pan = models.ForeignKey(TipoPan, on_delete=models.CASCADE, db_column='id_tipo_pan')
    tipo_relleno = models.ForeignKey(TipoRelleno, on_delete=models.CASCADE, db_column='id_tipo_relleno')
    imagen_quisco = models.ImageField(upload_to="rellenos/", blank=True, null=True)

    def __str__(self):
        return f"{self.categoria} - {self.tipo_pan} - {self.tipo_relleno}"

    class Meta:
        db_table = 'categoria_tipos_relleno_disponibles'
        unique_together = ('categoria', 'tipo_pan', 'tipo_relleno')
        verbose_name = 'Relleno Disponible por Categoría'
        verbose_name_plural = 'Rellenos Disponibles por Categoría'


class CategoriaTiposCoberturaColores(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    tipo_cobertura = models.ForeignKey(TipoCobertura, on_delete=models.CASCADE, db_column='id_tipo_cobertura')
    tipo_color = models.ForeignKey(TipoColores, on_delete=models.CASCADE, db_column='id_tipo_color')

    def __str__(self):
        return f"{self.categoria} - {self.tipo_cobertura} - {self.tipo_color}"

    class Meta:
        db_table = 'categoria_tipos_cobertura_colores'
        unique_together = ('categoria', 'tipo_cobertura', 'tipo_color')
        verbose_name = "Color Disponible por Cubierta"
        verbose_name_plural = "Colores Disponibles por Cubierta"


class CategoriaTiposCoberturaDecorados(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    tipo_cobertura = models.ForeignKey(TipoCobertura, on_delete=models.CASCADE, db_column='id_tipo_cobertura')
    tipo_decorado = models.ForeignKey(TiposDecoracion, on_delete=models.CASCADE, db_column='id_tipo_decorado')

    def __str__(self):
        return f"{self.categoria} - {self.tipo_cobertura} - {self.tipo_decorado}"

    class Meta:
        db_table = 'categoria_tipos_cobertura_decorados'
        unique_together = ('categoria', 'tipo_cobertura', 'tipo_decorado')
        verbose_name = 'Decorado Disponible por Cubierta'
        verbose_name_plural = 'Decorados Disponibles por Cubierta'


class DiasFestivos(models.Model):
    festivo = models.DateField()

    def __str__(self):
        return str(self.festivo)

    class Meta:
        db_table = 'dias_festivos'
        verbose_name = 'Dia Festivo'
        verbose_name_plural = 'Dias Festivos'


class HorarioEntrega(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Hora Inicio {self.hora_inicio} Hora Fin {self.hora_fin}"


    class Meta:
        db_table = 'horario_entrega'
        verbose_name = 'Horario Entrega'
        verbose_name_plural = 'Horarios Entregas'


class Extra(models.Model):
    descripcion = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = 'extras'
        verbose_name = 'Extra'
        verbose_name_plural = 'Extras'