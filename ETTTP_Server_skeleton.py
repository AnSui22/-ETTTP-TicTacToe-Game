'''
  ETTTP_Server_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept() #서버는 클라이언트 접속 대기
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        
        client_socket.send(str(start).encode()) #client socket에 start 변수를 인코딩하여 전송
        
        if start == 0: #서버가 먼저 시작하는 순서라면
            msg = 'SEND ETTTP/1.0\r\nHost:' + client_addr[0] + '\r\nFirst-Move: ME\r\n\r\n' #메시지는 서버가 먼저 시작한다고 작성
            
        elif start == 1: #클라이언트가 먼저 시작하는 순서라면
            msg = 'SEND ETTTP/1.0\r\nHost:'  + client_addr[0] + '\r\nFirst-Move: YOU\r\n\r\n' #메시지는 클라이언트가 먼저 시작한다고 작성

        client_socket.send(msg.encode()) #메시지를 인코딩하여 클라이언트 소켓에 전송
        
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        
        ack = client_socket.recv(1024).decode() #클라이언트 소켓이 전송한 first move ACK 메시지를 수신
        
        if not check_msg(ack, MY_IP): #ETTTP 형식에 맞지 않다면
          server_socket.close() #서버 소켓 닫고 종료
        
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()


