#!usr/bin/env/python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from random import randint
import threading
import socket
import os
import time
import sys
import struct #Para usar o Pack e Unpack

def receber_arquivo(nome,conn):
    buf = conn.recv(struct.calcsize('i')) #Calcula o tamanho de um pacote para inteiro
    tamNomeArquivo = struct.unpack('i', buf)[0] #Pega o tamanho do nome do arquivo
    nomeDoArquivo = conn.recv(tamNomeArquivo).decode()
    arq = open(nomeDoArquivo,'wb')
    while 1:
        dados = conn.recv(1024) #recebe de 1024 em 1024
        if not dados:
            conns.remove(conn) #remove se tiver desligado
            print("Processo desconectado...recalculando o líder...")
            break
        arq.write(dados)
        print("Identificador: " + str(dados))
    arq.close()

conns = set() #armazena as conexoes ativas
def _main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define o Socket
    origem = (sys.argv[1], int(sys.argv[2])) #argumentos
    s.bind(origem) #Aguardando conexao
    s.listen(7) #numero maximo de conexoes 
    print("ALGORITMO DE ELEIÇÃO EM ANEL \n")
    print("Ponto central em funcionamento...")	
    print(sys.argv)
    while True:
        conn, client = s.accept() #Estabelece uma conexao
        print("Conectado com o processo " + str(client))
        conns.add(conn) #adiciona a conexao ao set de conexoes
        #print(conns)
        thread = threading.Thread(target = receber_arquivo, args=("receber_arquivo",conn)) #Chama a funcao para receber o arquivo com threads
        thread.start()  #Inicia a thread em paralelo
    s.close()

if __name__ == '__main__':
    _main()

