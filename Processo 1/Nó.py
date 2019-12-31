#!usr/bin/env/python3
# -*- coding: utf-8 -*-
import socket
import os
import sys
import threading
import time
import struct #Para usar o Pack e Unpack
"""
FORMATO DOS PARAMETROS DE ENTRADA:
    sys.argv = [cliente.py, IP, PORTA, arquivo1.txt, arquivo2.mp3,...]
"""

def enviar_msg_servidor(nome, HOST, PORT, nomeDoArquivo):
    """Cria o Socket e Conecta"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Define o socket
    """Faz a conexao no servidor."""
    s.connect((HOST, PORT)) #Realiza a conexao no servidor
    tamNomeArquivo = len(nomeDoArquivo) #Pega o tamanho do nome do arquivo
    s.send(struct.pack('i', tamNomeArquivo)) #Envia o tamanho do nome do arquivo
    s.send(nomeDoArquivo.encode()) #Envia o nome do arquivo
    arq = open(nomeDoArquivo, 'rb') #Abre o arquivo para leitura binaria ('rb')
    for i in arq.readlines(): #Percorre as linhas do arquivo
        s.send(i) #Envia
    arq.close() #Fecha o arquivo aberto
    
    fim = input("Este processo esta ativo! Para desconectar digite 0: ")
    while fim != "0":
        s.sendall(fim) #fica escutando
    s.close() #Finaliza esta conexao de socket com o Servidor pois acabou o envio

def _main():
    for argumentos in sys.argv[3:]: #Percorre o nome dos arquivos
        print("O seu identificador foi enviado para o ponto central")
        """("enviar_msg_servidor") e o nome da thread, pois e o primeiro parametro"""
        thread = threading.Thread(target = enviar_msg_servidor, args=("enviar_msg_servidor",sys.argv[1],int(sys.argv[2]),argumentos)) #Chama a funcao para receber o identificador com threads
        thread.start()#Inicia a thread em paralelo

if __name__ == '__main__':
    _main()
    
