import cups
conn = cups.Connection()
printers = conn.getPrinters()

for printer in printers:
   print (printer,printers[printer]["device-uri"])

print(list(printers.keys())[0])

def print_file():
    file = "/home/nick/Documents/print.txt"
    print(file)
    printer_name = list(printers.keys())[0]
    conn.printFile(printer_name, file, "Project Report", {})
#return True

#print_file()
#print(printer_name)
