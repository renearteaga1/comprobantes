from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.template.loader import get_template

from weasyprint import HTML, CSS

from .models import Producto, Proveedor, Cliente, Credito, Consumo
from .forms import FacturaForm, ClienteForm
# Create your views here.

def index(request):
    name = 'Error'
    productos = Producto.objects.all()

    clientes = Cliente.objects.all()

    context = {
        'name':name,
        'productos':productos,
        'clientes':clientes,
    }
    if request.method == "POST":
        cliente_pk = request.POST.get('cliente_id')
        print(cliente_pk)
        return redirect('sitetest:consumo', cliente_id=cliente_pk)

    return render(request, 'sitetest/index.html', context)

def consumo(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    print(cliente)
    consumo_cliente = Credito.objects.filter(cliente=cliente)
    print(consumo_cliente)
    #if not consumo_cliente:
    #    form = FacturaForm()
    #else:
    #    consumo = Consumo.objects.latest('cliente', 'fecha')
    #    print(consumo)
    #    form = FacturaForm(instance=consumo)

    consumos = Consumo.objects.filter(cliente=cliente)
    #form = FacturaForm(instance=consumo)
    saldo = 1000
    for consumo in consumos:
        saldo = saldo - consumo.consumo
    context = {
        #'form' : form,
        'consumos':consumos,
        'saldo':saldo,
    }

    if request.method == 'POST':

        pass
        return render(request, 'sitetest/consumo.html', context)

    return render(request, 'sitetest/consumo.html', context)


def printer(request):
    if request.method == 'POST':
        text = request.POST.get('nombre')
        f = open('/home/nick/Documents/print.txt', 'w')
        f.write(str(text))
        f.close()
       # from . import printer
       # printer.print_file()
        import cups
        conn = cups.Connection()
        printers = conn.getPrinters()
        context={
        'name' : str(text)
        }
        template = get_template('sitetest/pdf.html')
        html = template.render(context)
        HTML(string=html).write_pdf('/home/nick/Documents/Django_Stuff/projectone/mysite/sitetest/print_pdf.pdf')
        file = "/home/nick/Documents/Django_Stuff/projectone/mysite/sitetest/print_pdf.pdf"
        #file = "/home/nick/Documents/print.txt"
        printer_name = list(printers.keys())[0]
        conn.printFile(printer_name, file, "Project Report", {})
        
    return redirect('sitetest:site_index')

def pdf(request):
    context={
    'name' : 'Josefo'
    }
 
    #import cups
    #conn = cups.Connection()
    #printers = conn.getPrinters()
 
    #file = "/home/nick/Documents/Django_Stuff/projectone/mysite/sitetest/print_pdf.pdf"
    #printer_name = list(printers.keys())[0]
    #conn.printFile(printer_name, file, "Project Report", {})
    return render(request, 'sitetest/pdf.html', context)
    #return redirect('sitetest:site_index')
  

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sitetest:site_index')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
