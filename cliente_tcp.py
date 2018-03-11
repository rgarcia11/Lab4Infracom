import socket
import threading
from tkinter import *
import time
############################################################
#             COMUNICACION CON EL SERVIDOR!
############################################################
print('comienzo')
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nombre_servidor = '52.234.215.61'
puerto_servidor = 5005
TAM_BUFFER = 1024
lista_archivos = []
estado_conexion = 0
inicio_descarga = 0
#Termina la conexion
def cerrar_conexion():
    estado_conexion = 0
    if cliente:
        cliente.shutdown(socket.SHUT_RDWR)
        cliente.close()

#Maneja la conexion con el servidor
def conexion_con_servidor():
    global lista_archivos
    global estado_conexion
    global inicio_descarga
    print('Intentare conectarme a {}:{}'.format(nombre_servidor, puerto_servidor))
    cliente.connect((nombre_servidor, puerto_servidor))
    print('conectado')
    estado_conexion = 1

    #saludo
    saludo = 'Hola'
    socket__conexion_servidor_cliente.sendto(str(saludo).encode(), (nombre_cliente, puerto_cliente))

    #Recibir e imprimir la lista de archivos
    lista_archivos = str(cliente.recv(TAM_BUFFER))
    if lista_archivos == b'Intente mas tarde':
        cerrar_conexion()
        return

    lista_archivos = lista_archivos[3:-2].split(", ")
    #print(a for a in lista_archivos)
    for a in lista_archivos:
        print(a)
    #print(type(lista_archivos))
    #print(lista_archivos)

    #Se inicia el proceso de timeout para que no demore mas de 15 s en escoger
    thread_timeout=threading.Thread(
        target=timeout_cliente
    )
    thread_timeout.start()

    #Se inicia el proceso de pedir un archivo!
    thread_archivo=threading.Thread(
        target=pedir_archivo
    )
    thread_archivo.start()


    print('Terminada comunicacion')

#peticion del archivo
def pedir_archivo():
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
            inicio_descarga = 1
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
            inicio_descarga = 0
            break
        else:
            mensaje = input('Por favor vuelva a ingresar el nombre del archivo, o deje vacio para terminar: ')
    cerrar_conexion()

def timeout_cliente():
    print('Llego a timeout')
    global estado_conexion
    global inicio_descarga
    while estado_conexion:
        time.sleep(15)
        print('reviso el timeout')
        if not inicio_descarga:
            print('hago timeout')
            cerrar_conexion()

print('inicio!')
conexion_con_servidor()

############################################################
#                       INTERFAZ!!
############################################################
#root=Tk()
#Label(root,text="Enter your name").grid(row=0,column=0) #Creating label
#a=Entry(root)           #creating entry box
#a.grid(row=7,column=8)
#Button(root,text="OK",command=xyz).grid(row=1,column=1)
#root.mainloop()           #important for closing th root=Tk()
