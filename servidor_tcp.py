import socket
import threading

bind_ip = '127.0.0.1'
bind_port = 5005

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((bind_ip, bind_port))
servidor.listen(5)

print ('Escuchando en (ip:puerto){}:{}'.format(bind_ip, bind_port))


def manejador_conexion(socket_cliente, nombre_cliente, puerto_cliente):
    request = socket_cliente.recv(1024)
    print ('Recibi: {}'.format(request))
    mensaje = 'ACK!'
    socket_cliente.sendto(mensaje.encode(),(nombre_cliente, puerto_cliente))
    #sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))
    socket_cliente.close()

while True:
    socket__conexion_servidor_cliente, direccion = servidor.accept()
    print ('Se acepto una conexion desde {}:{}'.format(direccion[0], direccion[1]))
    client_handler = threading.Thread(
        target=manejador_conexion,
        args=(socket__conexion_servidor_cliente, direccion[0], direccion[1])  #con la coma!!
    )
    client_handler.start()
