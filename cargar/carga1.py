import os

from .models import Comprobante

# path = '/home/nick/Documents'
# files = os.listdir(path)
# i = 1
# files_list = []
#
# for file in files:
#     #os.rename(os.path.join(path, file), os.path.join(path, str(i)+'.jpg'))
#     #file = os.path.join(path, file)
#     filename, fileext = os.path.splitext(file)
#     print(file)
#     print(filename)
#
#     '''renombrar archivos if file ext
#     print(fileext)
#     if fileext == '.pdf':
#         os.rename(os.path.join(path, file), os.path.join(path, str(i)+'.pdf'))
#     '''
#
#     files_list.append(filename)
#
#     i = i+1
# print(files_list)


def model_form_upload():
    carga = Comprobante(descripcion='Desc')
    form.save()
        #return redirect('sitetest:site_index')
        #return redirect('cargar:comprobante_list')

model_form_upload()
