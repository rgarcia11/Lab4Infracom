import socket

port = 'www', 'integralist', 'co.uk', 80

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nombre_servidor = '127.0.0.1'
puerto_servidor = 5005
cliente.connect((nombre_servidor, puerto_servidor))

mensaje = 'Este es un mensaje'
cliente.sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))

respuesta = cliente.recv(4096)

print (respuesta)

cliente.close()
