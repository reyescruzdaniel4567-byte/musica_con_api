from django.contrib import admin
from .models import Musico, TipoDeMusica, Instrumento

admin.site.register(Musico)
admin.site.register(TipoDeMusica)
admin.site.register(Instrumento)