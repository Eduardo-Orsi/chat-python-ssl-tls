import socket
import threading
import ssl

FORMATO = 'utf-8'
ADDR_CLIENT = ('localhost', 5051)
ADDR_SERVER = ('localhost', 3000)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('new.pem')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client = context.wrap_socket(client, server_hostname='localhost')
client.bind(ADDR_CLIENT)
client.connect(ADDR_SERVER)

def handle_mensagens():
    while(True):
        msg = client.read().decode(FORMATO)
        mensagem_splitada = msg.split("=")
        print(mensagem_splitada[1] + ": " + mensagem_splitada[2])

def enviar(mensagem):
    client.write(mensagem.encode(FORMATO))

def enviar_mensagem():
    while(True):
        mensagem = input()
        enviar("msg=" + mensagem)

def enviar_nome():
    nome = input('Digite seu nome: ')
    enviar("nome=" + nome)

def iniciar_envio():
    enviar_nome()
    enviar_mensagem()

def iniciar():
    thread1 = threading.Thread(target=handle_mensagens)
    thread2 = threading.Thread(target=iniciar_envio)
    thread1.start()
    thread2.start()

iniciar()