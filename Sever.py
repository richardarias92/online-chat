import socket
import threading

# Configuración del servidor
host = '192.168.101.4' #(direccion ficticia)
port = 55555

# Crear socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lista de clientes y sus nombres
clients = []
nicknames = []

# Función para difundir un mensaje a todos los clientes
def broadcast(message):
    for client in clients:
        client.send(message)

# Función para manejar la conexión de un cliente
def handle(client):
    while True:
        try:
            # Recibir mensaje del cliente y difundirlo
            message = client.recv(1024)
            broadcast(message)
        except:
            # Si hay algún error, eliminar al cliente y cerrar la conexión
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} se ha desconectado!'.encode('ascii'))
            break

# Función para aceptar conexiones de clientes y manejarlas
def receive():
    while True:
        # Aceptar conexión del cliente y agregarlo a la lista
        client, address = server.accept()
        print(f'Conectado con {str(address)}!')

        # Solicitar al cliente que ingrese su nombre y agregarlo a la lista de clientes y nombres
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Anunciar la conexión del cliente a todos los demás clientes
        print(f'Nombre del cliente es {nickname}!')
        broadcast(f'{nickname} se ha conectado!'.encode('ascii'))
        client.send('Conectado al servidor!'.encode('ascii'))

        # Iniciar un hilo para manejar la conexión del cliente
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Servidor está escuchando...')
receive()
