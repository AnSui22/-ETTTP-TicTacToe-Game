'''
  ETTTP_Client_skeleton.py
 
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

    SERVER_IP = '127.0.0.1' 
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    # socket() 함수를 사용하여 TCP 소켓 생성하고 클라이언트와 서버 간의 연결 설정
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server

        #recv() 함수를 사용하여 서버로부터 start 데이터 수신하고 문자열로 decode
        #디코딩된 문자열을 정수로 변환하여 start 변수에 할당
        start = int(client_socket.recv(1024).decode())
        
        ######################### Fill Out ################################
        # Send ACK

        #서버로부터 first mover decision 메시지를 ETTTP 형식으로 받고 문자열로 디코딩
        msg = client_socket.recv(1024).decode()

        
        if check_msg(msg, MY_IP): #메시지가 올바른 ETTTP 형식으로 왔다면
            if start == 0: # 서버가 먼저 시작하는 순서라면 
                ack = 'ACK ETTTP/1.0\r\nHost:' + SERVER_IP +'\r\nFirst-Move: YOU\r\n\r\n' #ACK 메시지는 서버가 먼저 시작한다고 작성
            elif start == 1: #클라이언트가 먼저 시작하는 순서라면
                ack = 'ACK ETTTP/1.0\r\nHost:'  + SERVER_IP+ '\r\nFirst-Move: ME\r\n\r\n' #ACK 메시지는 클라이언트가 먼저 시작한다고 작성
            client_socket.send(ack.encode()) #start 변수에 따라 다른 ACK 메시지 전송
        else:# 올바르지 않은 ETTTP 형식의 메시지가 왔다면
            client_socket.close() # 클라이언트 소켓 닫고 종료
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        

