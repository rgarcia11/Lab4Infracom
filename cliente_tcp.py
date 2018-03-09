import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nombre_servidor = '127.0.0.1'
puerto_servidor = 5005
TAM_BUFFER = 1024
print('Intentare conectarme a %s:%d'%(nombre_servidor, puerto_servidor))
cliente.connect((nombre_servidor, puerto_servidor))
print('conectado')
mensaje = input('Ingrese el nombre del archivo a descargar: ')
while mensaje:
    print('Pedi %s'%mensaje)
    cliente.sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))
    print('Mensaje enviado')
    archivo_recibir = cliente.recv(TAM_BUFFER)
    print ('Recibiendo archivo')
    print(type(archivo_recibir))
    print(archivo_recibir)
    if not archivo_recibir == 'No existe':
        f = open(mensaje, 'wb')
        while archivo_recibir:
            print('Recibiendo...')
            f.write(archivo_recibir)
            archivo_recibir = cliente.recv(TAM_BUFFER)
        print('Termine de recibir')
        f.close()
    else:
        mensaje = input('Por favor vuelva a ingresar el nombre del archivo')
    mensaje = ''
print('Terminada comunicacion')
cliente.close()
