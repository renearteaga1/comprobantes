import datetime
import os
import shutil

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.paginator import Paginator
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, JsonResponse

from weasyprint import HTML, CSS

from .models import Comprobante, ConteoComprobante, ErrorCarga, Oficio
from .forms import ComprobanteForm, CrearCarpetaForm

# Create your views here.
#user = User
def update(request):

    storage = messages.get_messages(request)
    tp = "NotasInventario"
    carpeta = 2011
    path = settings.MEDIA_ROOT
    path = os.path.join(path, tp)
    path = os.path.join(path, str(carpeta))
    documentos = os.listdir(path)
    errores = False
    files_error = []
    existe = False
    existe_file = False
    files_existe = []
    #files = os.listdir(os.path.join(comprobantes, "2011"))
    i = 0

    path_subir = os.path.join(tp, str(carpeta))
    instance_conteo = ConteoComprobante(usuario=request.user, conteo=len(documentos), tipo_documento=tp)
    instance_conteo.save()
    for f in documentos:
        file = str(f)
        filename, ext = file.split('.pdf')
        if tp == "Oficios":
            #VIEW IF CARGA SON Oficios
            carpeta = request.POST['institucion']
            institucion = request.POST['anio']
            respuesta = request.POST['respuesta']
            entrante = request.POST['entrante']
            descripcion = request.POST['descripcion']
            instance_conteo = ConteoComprobante(usuario=request.user, conteo=len(files), tipo_documento=tp)
            instance_conteo.save()
            for f in files:
                file = str(f)
                path_2 = os.path.join(path, str(tp))
                path_3 = os.path.join(path_2, carpeta)
                path_4 = os.path.join(path_3, institucion)
                print('pahtt3')
                print(path_3)
                print(path_4)

                filename, ext = file.split('.pdf')
                if not file.lower().endswith('.pdf'):
                    messages.warning(request, 'Archivo seleccionado no es pdf')
                    files.sort(reverse = True)
                    context = {
                        'carpetas':files,
                        'anios':files_1,
                        'tipo_documentos':tipo_documentos
                    }
                    return render(request, 'cargar/model_form_upload.html', context)
                elif carpeta == "" or carpeta == None:
                    messages.warning(request, 'Seleccione el año del documento')
                    return render(request, 'cargar/model_form_upload.html', context)
                else:
                    if len(filename) < 1:
                        files_error.append(filename+".pdf")
                        errores = True
                        instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error="Nombre archivo incorrecto", tipo_documento=tp)
                        instance_errores.save()
                        continue

                    try:
                        try:
                            existe = Oficio.objects.get(anio=carpeta, descripcion=filename, tipo=tp, institucion=institucion)
                        except:
                            existe = Oficio.objects.filter(anio=carpeta, descripcion=filename, tipo=tp, institucion=institucion)
                        if existe:
                            errores = True
                            existe_file = True
                            files_existe.append(existe)
                            error = str("Ya existe un archivo con el mismo nombre en carpeta %s, del anio %s" %(tp,carpeta))
                            instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error=error, tipo_documento=tp)
                            instance_errores.save()
                        else:
                            instance = Oficio(archivo=f, anio=carpeta, descripcion=descripcion, respuesta=respuesta, entrante=entrante, institucion=institucion, usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                            instance.save()
                            i = i + 1
                            exitosa = True
                    except:
                        instance = Oficio(comprobante=f, anio=carpeta, descripcion=descripcion, respuesta=respuesta, entrante=entrante,institucion=institucion, usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                        instance.save()
                        i = i + 1
                        exitosa = True

            if exitosa and i == len(files):
                instance_errores = ErrorCarga(conteo_id=instance_conteo)
                instance_errores.save()
                if int(i) > 1:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                else:
                    messages.success(request, "Carga exitosa de %i archivo" %i)
            elif errores or not i == len(files):
                if i > 0:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                else:
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                instance_conteo.conteo = i
                instance_conteo.errores = int((len(files)-i))
                instance_conteo.save()
                context = {
                    'carpetas':files,
                    'anios':files,
                    'tipo_documentos':tipo_documentos,
                    'errores': errores,
                    'files_error':files_error,
                    'existe':existe,
                    'existe_file':existe_file,
                    'files_existe':files_existe,
                }
                return render(request, 'cargar/error.html', context)

            return redirect('cargar:comprobante_list')
            print('oficioss')
        else:
            #VIEW IF CARGA SON COMPROBANTES O NI
            if not len(filename) == 6:
                files_error.append(filename+".pdf")
                errores = True
                instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error="Nombre archivo incorrecto", tipo_documento=tp)
                instance_errores.save()
                continue
            try:
                try:
                    existe = Comprobante.objects.get(anio=carpeta, descripcion=filename, tipo=tp)
                except:
                    existe = Comprobante.objects.filter(anio=carpeta, descripcion=filename, tipo=tp)
                if existe:
                    errores = True
                    existe_file = True
                    files_existe.append(existe)
                    error = str("Ya existe un archivo con el mismo nombre en carpeta %s, del anio %s" %(tp,carpeta))
                    instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error=error, tipo_documento=tp)
                    instance_errores.save()
                else:
                    instance = Comprobante(archivo=f, anio=carpeta, descripcion=filename, numero_comprobante=int(filename), usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                    instance.save()
                    i = i + 1
                    exitosa = True
            except:
                instance = Comprobante(archivo=os.path.join(path_subir, f), anio=carpeta, descripcion=filename, numero_comprobante=int(filename), usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                instance.save()
                i = i + 1
                exitosa = True
    if exitosa and i == len(documentos):
        instance_errores = ErrorCarga(conteo_id=instance_conteo)
        instance_errores.save()
        if int(i) > 1:
            messages.success(request, "Carga exitosa de %i archivos" %i)
        else:
            messages.success(request, "Carga exitosa de %i archivo" %i)
    elif errores or not i == len(documentos):
        if i > 0:
            messages.success(request, "Carga exitosa de %i archivos" %i)
            messages.error(request, "%i archivos no fueros cargados" %(len(documentos)-i))
        else:
            messages.error(request, "%i archivos no fueros cargados" %(len(documentos)-i))

        instance_conteo.conteo = i
        instance_conteo.errores = int((len(documentos)-i))
        instance_conteo.save()
        context = {
            'errores': errores,
            'files_error':files_error,
            'existe':existe,
            'existe_file':existe_file,
            'files_existe':files_existe,
        }
        return render(request, 'cargar/error.html', context)

    return redirect('cargar:comprobante_list')


@login_required(login_url='/login/')
@permission_required(('cargar.view_comprobantes','cargar.add_comprobantes'), raise_exception=True)
def model_form_upload(request):
    #path = '/home/nick/Documents/Django_Stuff/projectone/mysite/media/Comprobantes'
    storage = messages.get_messages(request)
    path = settings.MEDIA_ROOT
    tipo_documentos = os.listdir(path)

    files = os.listdir(path)
    #instituciones = os.listdir(os.path.join(path, file))
    existe = None
    existe_file = False
    files_existe = []
    errores = False
    exitosa = False
    i = 0
    files_error = []
    if request.method == 'POST':
        tp = request.POST['tipo_documento']
        carpeta = request.POST['anio']
        files = request.FILES.getlist('archivos')

        if tp == "Oficios":
            carpeta = request.POST['institucion']
            institucion = request.POST['anio']
            respuesta = request.POST['respuesta']
            entrante = request.POST['entrante']
            descripcion = request.POST['descripcion']
            instance_conteo = ConteoComprobante(usuario=request.user, conteo=len(files), tipo_documento=tp)
            instance_conteo.save()
            for f in files:
                file = str(f)
                path_2 = os.path.join(path, str(tp))
                path_3 = os.path.join(path_2, carpeta)
                path_4 = os.path.join(path_3, institucion)
                print('pahtt3')
                print(path_3)
                print(path_4)

                filename, ext = file.split('.pdf')
                if not file.lower().endswith('.pdf'):
                    messages.warning(request, 'Archivo seleccionado no es pdf')
                    files.sort(reverse = True)
                    context = {
                        'carpetas':files,
                        'anios':files_1,
                        'tipo_documentos':tipo_documentos
                    }
                    return render(request, 'cargar/model_form_upload.html', context)
                elif carpeta == "" or carpeta == None:
                    messages.warning(request, 'Seleccione el año del documento')
                    return render(request, 'cargar/model_form_upload.html', context)
                else:
                    if len(filename) < 1:
                        files_error.append(filename+".pdf")
                        errores = True
                        instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error="Nombre archivo incorrecto", tipo_documento=tp)
                        instance_errores.save()
                        continue

                    try:
                        try:
                            existe = Oficio.objects.get(anio=carpeta, descripcion=filename, tipo=tp, institucion=institucion)
                        except:
                            existe = Oficio.objects.filter(anio=carpeta, descripcion=filename, tipo=tp, institucion=institucion)
                        if existe:
                            errores = True
                            existe_file = True
                            files_existe.append(existe)
                            error = str("Ya existe un archivo con el mismo nombre en carpeta %s, del anio %s" %(tp,carpeta))
                            instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error=error, tipo_documento=tp)
                            instance_errores.save()
                        else:
                            instance = Oficio(archivo=f, anio=carpeta, descripcion=descripcion, respuesta=respuesta, entrante=entrante, institucion=institucion, usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                            instance.save()
                            i = i + 1
                            exitosa = True
                    except:
                        instance = Oficio(comprobante=f, anio=carpeta, descripcion=descripcion, respuesta=respuesta, entrante=entrante,institucion=institucion, usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                        instance.save()
                        i = i + 1
                        exitosa = True

            if exitosa and i == len(files):
                instance_errores = ErrorCarga(conteo_id=instance_conteo)
                instance_errores.save()
                if int(i) > 1:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                else:
                    messages.success(request, "Carga exitosa de %i archivo" %i)
            elif errores or not i == len(files):
                if i > 0:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                else:
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                instance_conteo.conteo = i
                instance_conteo.errores = int((len(files)-i))
                instance_conteo.save()
                context = {
                    'carpetas':files,
                    'anios':files,
                    'tipo_documentos':tipo_documentos,
                    'errores': errores,
                    'files_error':files_error,
                    'existe':existe,
                    'existe_file':existe_file,
                    'files_existe':files_existe,
                }
                return render(request, 'cargar/error.html', context)

            return redirect('cargar:comprobante_list')
            print('oficioss')
        else:
            #form = ComprobanteForm(request.POST, request.FILES)

            instance_conteo = ConteoComprobante(usuario=request.user, conteo=len(files), tipo_documento=tp)
            instance_conteo.save()

            #if form.is_valid():
            #instance = ModelWithFileField(file_field=request.FILES['file'])
            #instance.save()
            for f in files:
                if not str(f).lower().endswith('.pdf'):
                    messages.warning(request, 'Archivo seleccionado no es pdf')
                    #form = ComprobanteForm()

                    files.sort(reverse = True)
                    context = {
                        'carpetas':files,
                        'anios':carpeta,
                        'tipo_documentos':tipo_documentos
                    }
                    return render(request, 'cargar/model_form_upload.html', context)

            for f in files:
                file = str(f)
                #carpeta = form.cleaned_data['anio']
                path_2 = os.path.join(path, str(tp))
                path_3 = os.path.join(path, carpeta)
                print('pahtt3')
                print(path_3)

                filename, ext = file.split('.pdf')
                if carpeta == "" or carpeta == None:
                    messages.warning(request, 'Seleccione el año del documento')
                    return render(request, 'cargar/model_form_upload.html', context)
                else:
                    if not len(filename) == 6:
                        files_error.append(filename+".pdf")
                        errores = True
                        instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error="Nombre archivo incorrecto", tipo_documento=tp)
                        instance_errores.save()
                        continue

                    try:
                        try:
                            existe = Comprobante.objects.get(anio=carpeta, descripcion=filename, tipo=tp)
                        except:
                            existe = Comprobante.objects.filter(anio=carpeta, descripcion=filename, tipo=tp)
                        if existe:
                            errores = True
                            existe_file = True
                            files_existe.append(existe)
                            error = str("Ya existe un archivo con el mismo nombre en carpeta %s, del anio %s" %(tp,carpeta))
                            instance_errores = ErrorCarga(conteo_id=instance_conteo, archivo = str(filename+".pdf"), tipo_error=error, tipo_documento=tp)
                            instance_errores.save()
                        else:
                            instance = Comprobante(archivo=f, anio=carpeta, descripcion=filename, numero_comprobante=int(filename), usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                            instance.save()
                            i = i + 1
                            exitosa = True
                    except:
                        instance = Comprobante(archivo=f, anio=carpeta, descripcion=filename, numero_comprobante=int(filename), usuario=request.user, conteo_id=instance_conteo, tipo=tp)
                        instance.save()
                        i = i + 1
                        exitosa = True
            print(errores)
            if exitosa and i == len(files):
                instance_errores = ErrorCarga(conteo_id=instance_conteo)
                instance_errores.save()
                if int(i) > 1:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                else:
                    messages.success(request, "Carga exitosa de %i archivo" %i)
            elif errores or not i == len(files):
                if i > 0:
                    messages.success(request, "Carga exitosa de %i archivos" %i)
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                else:
                    messages.error(request, "%i archivos no fueros cargados" %(len(files)-i))
                instance_conteo.conteo = i
                instance_conteo.errores = int((len(files)-i))
                instance_conteo.save()
                context = {
                    #'form': form,
                    'carpetas':files,
                    'anios':files,
                    'tipo_documentos':tipo_documentos,
                    'errores': errores,
                    'files_error':files_error,
                    'existe':existe,
                    'existe_file':existe_file,
                    'files_existe':files_existe,
                }
                return render(request, 'cargar/error.html', context)

            return redirect('cargar:comprobante_list')

    else:
        #form = ComprobanteForm()
        pass
    # path = '/home/nick/Documents/Django_Stuff/projectone/mysite/media/Comprobantes'
    # files = os.listdir(path)
    # i = 1
    # Choices = [("","Seleccionar Carpeta")]
    # for carpeta in files:
    #         Choices.append((carpeta, carpeta))
    files.sort(reverse = True)
    context = {
        #'form': form,
        'carpetas':files,
        'anios':files,
        'tipo_documentos':tipo_documentos,
        'files_error':files_error,
    }

    return render(request, 'cargar/model_form_upload.html', context)

def ajax_cargar(request):
    data = dict()
    path = settings.MEDIA_ROOT

    path = os.path.join(path, str(request.GET.get('tipo_documento')))
    anio = os.path.join(path, str(request.GET.get('select_anio')))
    print(anio)
    if os.path.isdir(path):
        files = os.listdir(path)
        files.sort(reverse = True)
    else:
        files = ""
    if os.path.isdir(anio):
        instituciones = os.listdir(anio)
        instituciones.sort(reverse = True)
    else:
        instituciones = ""
    context = {
        'anios':files,
        'tipo_documentos':'hola',
        'instituciones':instituciones,
    }
    data['select_anios'] =  render_to_string('cargar/select_anio.html', context, request=request)
    data['select_institucion'] = render_to_string('cargar/select_institucion.html', context)
    return JsonResponse(data)

def comprobante_list(request):
    comprobantes = Comprobante.objects.order_by('descripcion')
    paginator = Paginator(comprobantes, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    comprobantes = paginator.get_page(page)
    anios = Comprobante.objects.values('anio').order_by('anio').distinct()

    value_anios = []
    for anio in anios:
        for k,v in anio.items():
            if not  v == None:
                value_anios.append(v)

    tipos = Comprobante.objects.values('tipo').order_by('tipo').distinct()
    tipo_oficio = Oficio.objects.values('tipo').order_by('tipo').distinct()
    tipo_inst = Oficio.objects.values('institucion').order_by('institucion').distinct()

    instituciones = []
    value_tipos = []
    for tipo in tipos:
        for k,v in tipo.items():
            if not v == "":
                value_tipos.append(v)
    for tipo in tipo_oficio:
        for k,v in tipo.items():
            if not v == "":
                value_tipos.append(v)
    for tipo in tipo_inst:
        for k,v in tipo.items():
            if not v == "":
                instituciones.append(v)

    # ntry.objects.order_by('pub_date').distinct('pub_date')
    context = {
        #'comprobantes' : comprobantes,
        'value_anios' : value_anios,
        'tipos': value_tipos,
        'instituciones': instituciones,
    }
    return render(request, 'cargar/comprobante_list.html', context)

def eliminar(request, pk):
    if request.method == 'POST':
        comprobante = Comprobante.objects.get(pk=pk)
        comprobante.delete()
    return redirect(request.META['HTTP_REFERER'])

# def nueva_carpeta(request,y):
#     #path = "/home/nick/Documents/"
#
#     if request.method == "POST":
#         form = CrearCarpetaForm(request.POST)
#         if form.is_valid():
#
#
#     return redirect('cargar:comprobante_list')

@login_required(login_url='/login/')
@permission_required(('cargar.delete_comprobantes','cargar.add_comprobantes'), raise_exception=True)
def delete_folder (request):
    storage = messages.get_messages(request)
    path = settings.MEDIA_ROOT
    tipo_documentos = os.listdir(path)
    path = os.path.join(path, 'Comprobantes')
    files = os.listdir(path)

    files.sort(reverse = True)
    context = {
        'anios':files,
        'tipo_documentos':tipo_documentos,
    }
    return render(request, 'cargar/delete_folder.html', context)

@login_required(login_url='/login/')
@permission_required(('cargar.delete_comprobantes','cargar.add_comprobantes'), raise_exception=True)
def eliminar_carpeta(request, slug):
    storage = messages.get_messages(request)
    form = CrearCarpetaForm()
    path = settings.MEDIA_ROOT
    if request.method == 'POST':
        tipo_documento = request.POST['tipo_documento']
    else:
        tipo_documento = request.GET.get('tipo_documento')
    path = os.path.join(path, str(tipo_documento))
    files = os.listdir(path)
    data = dict()

    if request.method == 'POST':

        try:
            os.rmdir(os.path.join(path, str(slug)))
            files = os.listdir(path)
            data['form_valid'] = True
            data['carpeta_lista'] = render_to_string('cargar/carpetas_lista.html',{'anios':files})

        except:
            comprobantes = Comprobante.objects.filter(anio=str(slug))
            for comprobante in comprobantes:
                comprobante.delete()
            shutil.rmtree(os.path.join(path, str(slug)), ignore_errors=True)
            files = os.listdir(path)
            data['form_valid'] = True
            data['carpeta_lista'] = render_to_string('cargar/carpetas_lista.html',{'anios':files})
    else:
        if len(os.listdir(os.path.join(path, str(slug))) ) == 0:
            context={
                'carpeta':str(slug),
                'data':False,
                'tipo_documento':tipo_documento,
                }
        else:
            context={
                'carpeta':str(slug),
                'data':True,
                'tipo_documento':tipo_documento,
                }

        data['html_data'] = render_to_string('cargar/modal-delete.html',context, request=request)

    return JsonResponse(data)

def carpeta(request):
    storage = messages.get_messages(request)
    form = CrearCarpetaForm()
    path = settings.MEDIA_ROOT
    tipo_documentos = os.listdir(path)
    if request.method == "POST":
        form = CrearCarpetaForm(request.POST)
        if form.is_valid():
            #year = form.cleaned_data['anio']
            nombre = form.cleaned_data['nombre_carpeta'].lower()
            tipo_documento = request.POST['tipo_documento']

            path_1 = os.path.join(path, str(tipo_documento))
            path_carpeta = os.path.join(path_1, nombre)

            try:
                os.makedirs(path_carpeta)
            except OSError:
                messages.warning(request, path_carpeta)
                return redirect('cargar:carpeta')
            else:
                print ("Successfully created the directory %s " % path)
            return redirect('cargar:index')

    context = {
        'form':form,
        'message':storage,
        'tipo_documentos':tipo_documentos
    }
    return render(request, 'cargar/carpeta.html', context)

def carpeta_oficio(request):
    storage = messages.get_messages(request)
    form = CrearCarpetaForm()
    path = settings.MEDIA_ROOT
    tipo_documentos = os.listdir(path)
    if request.method == "POST":
        year = request.POST['anio']
        nombre = request.POST['nombre_carpeta'].lower()
        tipo_documento = request.POST['tipo-documento']

        path_1 = os.path.join(path, str(tipo_documento))
        path_carpeta = os.path.join(path_1, year)
        path_institucion = os.path.join(path_carpeta, nombre)

        try:
            os.makedirs(path_institucion)
            messages.success(request, "Carpeta %s creada correctamente."%nombre)
        except OSError:
            messages.warning(request, path_institucion)
            return redirect('cargar:carpeta')
        else:
            print ("Successfully created the directory %s " % path)
        return redirect('cargar:index')

    context = {
        'form':form,
        'message':storage,
        'tipo_documentos':tipo_documentos
    }
    return render(request, 'cargar/carpeta_oficio.html', context)

def busqueda(request):
    storage = messages.get_messages(request)
    oficio = False
    query = request.GET.get('q')
    query_anio = request.GET.get('a')
    query_tipo = request.GET.get('t')
    query_inst = request.GET.get('i')

    if query == "" and query_anio == "" and query_tipo:
        messages.warning(request, 'Seleccione un tipo de documento y año para la consulta')
        return redirect('cargar:comprobante_list')
    elif query_anio == "" and query_tipo == "":
        messages.warning(request, 'Seleccione un tipo de documento y año para la consulta')
        return redirect('cargar:comprobante_list')
    elif query == "" and query_tipo == "":
        messages.warning(request, 'Seleccione un tipo de documento y año para la consulta')
        return redirect('cargar:comprobante_list')

    if query_tipo == "Oficios":
        try:
            results = Oficio.objects.filter(anio=query_anio, tipo=query_tipo, institucion=query_inst).filter(descripcion__icontains=query).order_by('-uploaded_at')
            oficio = True
        except:
            results = Oficio.objects.filter(institucion=query_inst).order_by('-uploaded_at')
            oficio = True
    else:
        try:
            results = Comprobante.objects.filter(anio=query_anio, tipo=query_tipo).filter(descripcion__endswith=query).order_by('numero_comprobante')
        except:
            results = Comprobante.objects.filter(anio=query_anio).order_by('numero_comprobante')

    paginator = Paginator(results, 15)
    page = request.GET.get('page')
    comprobantes = paginator.get_page(page)
    anios = Comprobante.objects.values('anio').order_by('anio').distinct()
    value_anios = []
    for anio in anios:
        for k,v in anio.items():
            value_anios.append(v)
    tipos = Comprobante.objects.values('tipo').order_by('tipo').distinct()
    tipo_oficio = Oficio.objects.values('tipo').order_by('tipo').distinct()

    value_tipos = []
    for tipo in tipos:
        for k,v in tipo.items():
            if not v == "":
                value_tipos.append(v)

    for tipo in tipo_oficio:
        for k,v in tipo.items():
            if not v == "":
                value_tipos.append(v)
    context = {
        'comprobantes':comprobantes,
        'value_anios':value_anios,
        'query':query,
        'anio':query_anio,
        'tipos':value_tipos,
        'oficio':oficio,
    }
    return render(request, 'cargar/comprobante_list.html', context)

def reporte(request):
    storage = messages.get_messages(request)
    resultados = False
    date = datetime.datetime.now()  + datetime.timedelta(days=1)
    users = User.objects.all()
    query = ""
    total_cargas = 0
    total_errores = 0
    if request.method == 'POST':
        resultados = True
        fecha_inicial = request.POST['fechaInicial']
        fecha_final = request.POST['fechaFinal']
        usuario = request.POST['usuario']
        if fecha_inicial == "":
            fecha_inicial = fecha_final
            messages.warning(request, "No selecciono fecha de inicio")
        if usuario == "None":
            query = ConteoComprobante.objects.filter(uploaded_date__range=[fecha_inicial,fecha_final]).order_by("-uploaded_date")
        else:
            query = ConteoComprobante.objects.filter(usuario=usuario,uploaded_date__range=[fecha_inicial,fecha_final]).order_by("-uploaded_date")

        for carga in query:
            total_cargas = total_cargas + carga.conteo
            total_errores = total_errores + carga.errores

    context ={
        'resultados':resultados,
        'date':date.strftime("%Y-%m-%d"),
        'users':users,
        'consulta':query,
        'total_cargas':total_cargas,
        'total_errores':total_errores,
    }
    return render(request, 'cargar/reporte.html', context)

def reporte_errores(request, pk):
    query = ErrorCarga.objects.filter(conteo_id=pk)
    errores_reporte = True
    context = {
        'errores_reporte':errores_reporte,
        'dato_errores':query,
    }
    return render(request, 'cargar/error.html', context)

def login_view(request):
    storage = messages.get_messages(request)
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('cargar:comprobante_list')

    else:
        messages.error(request, 'Usuario y contrasena no validos.')

        return redirect('cargar:index')
    context = {
        'message':storage
    }
    print('login')
    return render(request, 'cargar:comprobante_list', context)

def logout_view(request):
    logout(request)
    return redirect('cargar:comprobante_list')

def password_reset(request):
    pass
