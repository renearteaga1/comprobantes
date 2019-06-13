import os, shutil

path = "/home/nick/Documents/Django_Stuff/projectone/mysite/media/NotasInventario/2011/"
files = os.listdir(path)
for file in files:
    if os.path.isfile(os.path.join(path, file)):
        if file == "1.pdf":

            filename, ext = file.split('.pdf')
            print(filename)
            for i in range(2,5001):
                f = str(i)+'.pdf'
                shutil.copyfile(os.path.join(path, file), os.path.join(path, str(f)))
