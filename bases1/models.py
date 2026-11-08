from django.db import models

class TipoDeMusica(models.Model):
    nombre_de_la_musica = models.CharField(max_length=50) 
    tipo_de_musica = models.CharField(max_length=30)       
    banda_de_musica = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo de música"
        verbose_name_plural = "Tipos de música"

    def __str__(self):
        return f'{self.nombre_de_la_musica} ({self.tipo_de_musica})'


class Musico(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    fecha_fallecimiento = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True) 
    
   
    genero_principal = models.ForeignKey(
        TipoDeMusica, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="musicos_principales"
    )
    genero_tipico = models.ForeignKey(
        TipoDeMusica, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="musicos_tipicos"
    )

    class Meta:
        verbose_name = "Músico"
        verbose_name_plural = "Músicos"

    def __str__(self):
        if self.fecha_fallecimiento:
            return f'{self.nombre} {self.apellido} ({self.fecha_nacimiento.year} - {self.fecha_fallecimiento.year})'
        return f'{self.nombre} {self.apellido} (Nació: {self.fecha_nacimiento.year})'


class Instrumento(models.Model):
    nombre_del_instrumento = models.CharField(max_length=50) 
    tipo_de_instrumento = models.CharField(max_length=50) 
    descripcion = models.TextField(blank=True) 
    musicos = models.ManyToManyField(Musico, blank=True, related_name="instrumentos")
    class Meta:
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"

    def __str__(self):
        return f'{self.nombre_del_instrumento} ({self.tipo_de_instrumento})'
