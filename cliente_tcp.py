import socket
import threading
import tkinter as tk

############################################################
#             COMUNICACION CON EL SERVIDOR!
############################################################

def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nombre_servidor = '52.234.215.61'
puerto_servidor = 5005
TAM_BUFFER = 1024
print('Intentare conectarme a {}:{}'.format(nombre_servidor, puerto_servidor))
cliente.connect((nombre_servidor, puerto_servidor))
print('conectado')
#Recibir e imprimir la lista de archivos
lista_archivos = str(cliente.recv(TAM_BUFFER))
lista_archivos = lista_archivos[3:-2].split(", ")
#print(a for a in lista_archivos)
for a in lista_archivos:
    print(a)
#print(type(lista_archivos))
#print(lista_archivos)

#peticion del archivo
mensaje = input('Ingrese el nombre del archivo a descargar, o deje vacio para terminar: ')
#Este while es para tener comunicacion mientras no escriba vacio
while mensaje:
    print('Pedi {}'.format(mensaje))
    cliente.sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))
    print('Mensaje enviado')
    tam_archivo = cliente.recv(TAM_BUFFER)
    print(tam_archivo)
    if not tam_archivo == b'No existe':
        tam_archivo = int(tam_archivo)
        print('Tam archivo: {}'.format(tam_archivo))
        tam_actual = 0
        buff = b""
        print('Recibiendo:')
        with open(mensaje, 'wb') as f:
            while tam_actual < tam_archivo:
                print('Tamanho actual del archivo: {}'.format(tam_actual))
                print('Tamanho del archivo: {}'.format(tam_archivo))
                progreso = tam_actual/tam_archivo*100
                print('Recibiendo... {}%'.format(progreso))
                archivo_recibir = cliente.recv(TAM_BUFFER)
                if not archivo_recibir:
                    break
                if len(archivo_recibir) + tam_actual > tam_archivo:
                    archivo_recibir = archivo_recibir[:tam_archivo-tam_actual]
                buff += archivo_recibir
                tam_actual += len(archivo_recibir)
                f.write(archivo_recibir)
        print('Termine de recibir')
        break
    else:
        mensaje = input('Por favor vuelva a ingresar el nombre del archivo, o deje vacio para terminar: ')
cliente.close()
print('Terminada comunicacion')


############################################################
#                       INTERFAZ!!
############################################################
