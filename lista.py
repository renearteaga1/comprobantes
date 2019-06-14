import os

path = "/home/nick/Documents/Django_Stuff/projectone/mysite/media/NotasInventario/2011"
#path = "E:/i/new"
documentos = os.listdir(path)
carpeta = 2011
tp = "NotasInventario"
error_nombres = []

i = 1
for d in documentos:
    filename, ext = d.split('.pdf')
    list.append({'f':d,'carpeta':carpeta,'filename':filename,'numero_comprobante':int(filename),'tp':tp})

with open("lista_notas.py", "w") as text_file:
    print(f"list= {list}", file=text_file)
