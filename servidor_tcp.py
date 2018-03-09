import socket
import threading
import os.path

#Este servidor recibe conexion de un solo cliente al tiempo (no hay threading)
#ip y puertos del servidor
bind_ip = '127.0.0.1'
bind_port = 5005
TAM_BUFFER = 1024
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((bind_ip, bind_port))
servidor.listen(5)

print ('Escuchando en (ip:puerto){}:{}'.format(bind_ip, bind_port))

#funcion para usar threading.
def manejador_conexion(socket_cliente, nombre_cliente, puerto_cliente):
    request = socket_cliente.recv(1024)
    print ('Recibi: {}'.format(request))
    mensaje = 'ACK!'
    socket_cliente.sendto(mensaje.encode(),(nombre_cliente, puerto_cliente))
    #sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))
    socket_cliente.close()

while True:
    print('aceptando conexion!')
    socket__conexion_servidor_cliente, direccion = servidor.accept()
    nombre_cliente = direccion[0]
    puerto_cliente = direccion[1]
    print ('Se acepto una conexion desde {}:{}'.format(direccion[0], direccion[1]))
    ##Esto inicia el threading en caso de que se espere mas de un cliente
    #client_handler = threading.Thread(
    #    target=manejador_conexion,
    #    args=(socket__conexion_servidor_cliente, direccion[0], direccion[1])  #con la coma!!
    #)
    #client_handler.start()
    peticion = socket__conexion_servidor_cliente.recv(TAM_BUFFER)
    print ('Recibi: {}'.format(peticion))
    if os.path.isfile(peticion):
        f = open(peticion, 'rb')
        archivo_enviar = f.read(TAM_BUFFER)
        while archivo_enviar:
            socket__conexion_servidor_cliente.send(archivo_enviar)
            archivo_enviar = f.read(TAM_BUFFER)
        f.close()
        socket__conexion_servidor_cliente.shutdown(socket.SHUT_WR)
    else:
        socket__conexion_servidor_cliente.sendto('No existe'.encode(), (nombre_cliente, puerto_cliente))
    socket__conexion_servidor_cliente.close()
