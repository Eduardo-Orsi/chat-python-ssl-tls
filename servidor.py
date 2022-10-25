import socket
import threading
import time
from datetime import datetime
import ssl

SERVER_IP = 'localhost'
PORT = 3000
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('new.pem', 'private.key')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server = context.wrap_socket(server, server_side=True)
server.bind(ADDR)

conexoes = []
mensagens = []

def enviar_mensagem_individual(conexao):
    print(f"[ENVIANDO] Enviando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):
        mensagem_de_envio = "msg=" + mensagens[i]
        conexao['conn'].write(mensagem_de_envio.encode(FORMATO))
        conexao['last'] = i + 1
        time.sleep(0.2)

def enviar_mensagem_todos():
    global conexoes
    for conexao in conexoes:
        enviar_mensagem_individual(conexao)

def tratar_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes
    global mensagens
    nome = False

    while(True):
        msg = conn.read().decode(FORMATO)
        if(msg):
            if(msg.startswith("nome=")):
                mensagem_separada = msg.split("=")
                nome = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao)
                enviar_mensagem_individual(mapa_da_conexao)
            elif(msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                data_e_hora_atuais = datetime.now()
                data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
                mensagem = nome +" " + data_e_hora_em_texto + "=" + mensagem_separada[1]
                mensagens.append(mensagem)
                enviar_mensagem_todos()

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen(5)
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=tratar_clientes, args=(conn, addr))
        thread.start()

start()