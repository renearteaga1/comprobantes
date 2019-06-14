from lista_notas import *
#list = [{'key':'uno','value': 1,'descripcion':'texto'},{'key':'dos','value': 2,'descripcion':'texto'}]
# for l in list:
#     # for i in l.items():
#         # if k == "descripcion":
#         #     print("%s => %s" %(k,v))
#         # descripcion = l['descripcion']
#         # print(descripcion)
#     descripcion = l['descripcion']
#     key = l['value']
#     print(descripcion)
#     print(key)
print(lista_doc)
for l in lista_doc:
    # for i in l.items():
        # if k == "descripcion":
        #     print("%s => %s" %(k,v))
        # descripcion = l['descripcion']
        # print(descripcion)
    descripcion = l['f']
    key = l['carpeta']
    print(descripcion)
    print(key)
