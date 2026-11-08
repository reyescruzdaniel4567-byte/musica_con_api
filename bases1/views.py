from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Musico, TipoDeMusica, Instrumento
from datetime import datetime

from django.shortcuts import render
from .models import Musico, TipoDeMusica, Instrumento
from ytmusicapi import YTMusic

from ytmusicapi import YTMusic

def index(request):
    # 1. Traer los músicos normales de tu base de datos de PostgreSQL
    musicos_db = Musico.objects.all()
    
    # 2. Inicializar el buscador automático de YouTube Music
    yt = YTMusic()
    
    musicos_con_videos = []
    
    for m in musicos_db:
        enlace_video = "#"
        nombre_cancion = ""
        
        try:
            # Buscamos el nombre completo del artista más su tema o grupo de referencia
            termino_busqueda = f"{m.nombre} {m.apellido}"
            if m.genero_principal:
                termino_busqueda += f" {m.genero_principal.nombre_de_la_musica}"
            
            # Hacer la consulta de canciones en la API (trae el primer resultado más relevante)
            resultados = yt.search(query=termino_busqueda, filter="songs", limit=1)
            
            if resultados:
                cancion = resultados[0]
                # CORRECCIÓN DEFINITIVA: Formato estructurado para evitar URLs pegadas
                enlace_video = f"https://music.youtube.com/watch?v={cancion['videoId']}"
                nombre_cancion = cancion['title']
        except Exception:
            # Si falla el internet o no encuentra nada, continúa sin dañar la página
            pass
            
        # Empaquetamos el objeto original con la información externa
        musicos_con_videos.append({
            'objeto': m,
            'enlace_video': enlace_video,
            'nombre_cancion': nombre_cancion
        })

    context = {
        'musicos_con_videos': musicos_con_videos,
        'generos': TipoDeMusica.objects.all(),
        'instrumentos': Instrumento.objects.all(),
    }
    return render(request, 'bases1/index.html', context)
# ==========================================
# 2. CRUD DE MÚSICOS
# ==========================================
def crear_musico(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nac_str = request.POST.get('fecha_nacimiento')
        fecha_fal_str = request.POST.get('fecha_fallecimiento')
        descripcion = request.POST.get('descripcion')
        genero_id = request.POST.get('genero_principal')

        fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date() if fecha_nac_str else None
        fecha_fallecimiento = datetime.strptime(fecha_fal_str, '%Y-%m-%d').date() if fecha_fal_str else None
        genero = TipoDeMusica.objects.get(id=genero_id) if genero_id else None

        if nombre and apellido and fecha_nacimiento:
            Musico.objects.create(
                nombre=nombre, apellido=apellido,
                fecha_nacimiento=fecha_nacimiento, fecha_fallecimiento=fecha_fallecimiento,
                descripcion=descripcion, genero_principal=genero
            )
            messages.success(request, "Músico creado exitosamente.")
            return redirect('bases1')
    
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/crear_musico.html', {'generos': TipoDeMusica.objects.all()})

def editar_musico(request, pk):
    musico = get_object_or_404(Musico, pk=pk)
    if request.method == 'POST':
        musico.nombre = request.POST.get('nombre')
        musico.apellido = request.POST.get('apellido')
        fecha_nac_str = request.POST.get('fecha_nacimiento')
        fecha_fal_str = request.POST.get('fecha_fallecimiento')
        musico.descripcion = request.POST.get('descripcion')
        genero_id = request.POST.get('genero_principal')

        if fecha_nac_str:
            musico.fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
        musico.fecha_fallecimiento = datetime.strptime(fecha_fal_str, '%Y-%m-%d').date() if fecha_fal_str else None
        musico.genero_principal = TipoDeMusica.objects.get(id=genero_id) if genero_id else None
        musico.save()
        messages.success(request, "Músico actualizado correctamente.")
        return redirect('bases1')
    
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/editar_musico.html', {'musico': musico, 'generos': TipoDeMusica.objects.all()})

def eliminar_musico(request, pk):
    musico = get_object_or_404(Musico, pk=pk)
    if request.method == 'POST':
        musico.delete()
        messages.success(request, "Músico eliminado con éxito.")
        return redirect('bases1')
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/confirmar_eliminar.html', {'objeto': musico, 'tipo': 'Músico'})


# ==========================================
# 3. CRUD DE TIPOS DE MÚSICA
# ==========================================
def crear_genero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_de_la_musica')
        tipo = request.POST.get('tipo_de_musica')
        banda = request.POST.get('banda_de_musica')
        
        if nombre and tipo and banda:
            TipoDeMusica.objects.create(nombre_de_la_musica=nombre, tipo_de_musica=tipo, banda_de_musica=banda)
            messages.success(request, "Género musical registrado.")
            return redirect('bases1')
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/crear_genero.html')

def editar_genero(request, pk):
    genero = get_object_or_404(TipoDeMusica, pk=pk)
    if request.method == 'POST':
        genero.nombre_de_la_musica = request.POST.get('nombre_de_la_musica')
        genero.tipo_de_musica = request.POST.get('tipo_de_musica')
        genero.banda_de_musica = request.POST.get('banda_de_musica')
        genero.save()
        messages.success(request, "Género actualizado.")
        return redirect('bases1')
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/crear_genero.html', {'genero': genero})

def eliminar_genero(request, pk):
    genero = get_object_or_404(TipoDeMusica, pk=pk)
    if request.method == 'POST':
        genero.delete()
        messages.success(request, "Género eliminado.")
        return redirect('bases1')
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/confirmar_eliminar.html', {'objeto': genero, 'tipo': 'Género/Banda'})


# ==========================================
# 4. CRUD DE INSTRUMENTOS
# ==========================================
def crear_instrumento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_del_instrumento')
        tipo = request.POST.get('tipo_de_instrumento')
        desc = request.POST.get('descripcion')
        musicos_ids = request.POST.getlist('musicos')

        if nombre and tipo:
            inst = Instrumento.objects.create(nombre_del_instrumento=nombre, tipo_de_instrumento=tipo, descripcion=desc)
            inst.musicos.set(musicos_ids)
            messages.success(request, "Instrumento registrado con éxito.")
            return redirect('bases1')
            
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/crear_instrumento.html', {'musicos': Musico.objects.all()})

def editar_instrumento(request, pk):
    inst = get_object_or_404(Instrumento, pk=pk)
    if request.method == 'POST':
        inst.nombre_del_instrumento = request.POST.get('nombre_del_instrumento')
        inst.tipo_de_instrumento = request.POST.get('tipo_de_instrumento')
        inst.descripcion = request.POST.get('descripcion')
        inst.musicos.set(request.POST.getlist('musicos'))
        inst.save()
        messages.success(request, "Instrumento actualizado.")
        return redirect('bases1')
        
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/editar_instrumento.html', {'instrumento': inst, 'musicos': Musico.objects.all()})

def eliminar_instrumento(request, pk):
    inst = get_object_or_404(Instrumento, pk=pk)
    if request.method == 'POST':
        inst.delete()
        messages.success(request, "Instrumento eliminado.")
        return redirect('bases1')
    # Modificado con el prefijo bases1/
    return render(request, 'bases1/confirmar_eliminar.html', {'objeto': inst, 'tipo': 'Instrumento'})
