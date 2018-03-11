import socket
import threading
import os.path
import time

#ip y puertos del servidor
bind_ip = '127.0.0.1'
bind_port = 5005
TAM_BUFFER = 1024
MAX_THREADS = 100
NUM_THREADS = 0
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((bind_ip, bind_port))
servidor.listen(5)

print ('Escuchando en (ip:puerto){}:{}'.format(bind_ip, bind_port))

#funcion para usar threading.
def manejador_conexion(socket__conexion_servidor_cliente, nombre_cliente, puerto_cliente):
    #se envia la lista de archivos primero
    lista_archivos = [a for a in os.listdir() if os.path.isfile(a)]
    lista_archivos.remove('cliente_tcp.py')
    lista_archivos.remove('servidor_tcp.py')
    lista_archivos.remove('Lab4Redes.rdp')
    socket__conexion_servidor_cliente.sendto(str(lista_archivos).encode(), (nombre_cliente, puerto_cliente))

    #se recibe la peticion del archivo a enviar
    peticion = socket__conexion_servidor_cliente.recv(TAM_BUFFER)
    print ('Recibi: {}'.format(peticion))
    while not os.path.isfile(peticion):
        socket__conexion_servidor_cliente.sendto('No existe'.encode(), (nombre_cliente, puerto_cliente))
        peticion = socket__conexion_servidor_cliente.recv(TAM_BUFFER)

    tam_archivo = os.path.getsize(peticion)
    socket__conexion_servidor_cliente.sendto(str(tam_archivo).encode(), (nombre_cliente, puerto_cliente))
    with open(peticion, 'rb') as f:
        archivo_enviar = f.read(TAM_BUFFER)
        while archivo_enviar:
            socket__conexion_servidor_cliente.send(archivo_enviar)
            archivo_enviar = f.read(TAM_BUFFER)
    socket__conexion_servidor_cliente.shutdown(socket.SHUT_WR)

    socket__conexion_servidor_cliente.close()
    print('Conexion cerrada con {}:{}'.format(nombre_cliente, puerto_cliente))

def manejador_clientes():
    while True:
        print('aceptando conexion!')
        socket__conexion_servidor_cliente, direccion = servidor.accept()
        nombre_cliente = direccion[0]
        puerto_cliente = direccion[1]
        print ('Se acepto una conexion desde {}:{}'.format(direccion[0], direccion[1]))
        ##Esto inicia el threading en caso de que se espere mas de un cliente
        thread_cliente = threading.Thread(
            target=manejador_conexion,
            args=(socket__conexion_servidor_cliente, nombre_cliente, puerto_cliente,)  #con la coma!!
        )
        thread_cliente.start()
        t.join(15)

thread_generador_clientes = threading.Thread(
    target=manejador_clientes
)
thread_generador_clientes.start()
while True:
    print('Numero de conexiones activas: {}'.format(threading.activeCount()))
    time.sleep(3)
