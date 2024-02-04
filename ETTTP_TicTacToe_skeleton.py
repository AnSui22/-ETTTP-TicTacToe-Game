'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################

        msg =  self.socket.recv(1024).decode() # get message using socket
        
        # New-Move 추출
        
        msg = msg.replace("\\r\\n", " ") #"\\r\\n" 를 공백으로 대체
        msg = msg.replace(":", " ") #":"를 공백으로 대체
        lines = msg.split(" ") #공백을 기준으로 split 해서 리스트에 저장
        
        move_line = lines[5] #받은 메시지에서 추출한 좌표  ex"(1,2)"
        row = int(move_line[1:2]) #행좌표 추출
        col = int(move_line[3:4]) #열좌표 추출
        
        ack = 'ACK ETTTP/1.0\r\nHost:' + self.send_ip +'\r\nNew-Move:'+ move_line +'\r\n\r\n' #msg에 대한 ACK 메시지 작성
        
        if check_msg(msg , self.recv_ip): #메시지가 ETTTP 형식에 맞다면
            msg_valid_check = False # Message is valid
        else:
            msg_valid_check = True #Message is not valid

        
        if msg_valid_check: # Message is not valid
            self.socket.close() #소켓 닫고
            self.quit() #종료
            return
        
        else:  # If message is valid - send ack, update board and change turn
            self.socket.send(ack.encode()) #작성한 ACK 전송
            loc = row * 3 + col # received next-move
            
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        d_msg_lines = d_msg.replace("\r\n", " ") #"\r\n" 를 공백으로 대체
        d_msg_lines = d_msg_lines.replace(":", " ") #":" 를 공백으로 대체
        lines = d_msg_lines.split(" ") #공백을 기준으로 d_msg 문자열 split 해서 lines 리스트에 저장
        
        move_line = lines[5] #받은 메시지에서 추출한 좌표  ex"(1,2)"
        row = int(move_line[1:2]) #행좌표 추출
        col = int(move_line[3:4]) #열좌표 추출

        user_move = row * 3 + col  # received next-move

        if self.board[user_move] != 0: #보드가 이미 채워져 있다면
            return #do nothing

        '''
        Send message to peer
        '''
        self.socket.send(d_msg.encode()) #peer 에게 메시지 전송

        '''
        Get ack
        '''
        ack = self.socket.recv(1024).decode() # ack 메시지 받음

        if check_msg(ack, self.recv_ip): #ETTTP 형식에 맞다면
            loc = row * 3 + col # peer's move, from 0 to 8
        else: #맞지 않다면
            return #do nothing

    
        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3) #selected button 의 행과 열
        
        ###################  Fill Out  #######################

        # send message and check ACK

        #selected button의 행과 열 좌표를 포함한 new-move msg 작성
        msg = "SEND ETTTP/1.0\\r\\nHost:"+ self.send_ip +"\\r\\nNew-Move:(" + str(row) +","+ str(col)+ ")\\r\\n\\r\\n" 
        
        self.socket.send(msg.encode()) #작성한 메시지 전송

        ack = self.socket.recv(1024).decode() #ack 받음

        if check_msg(ack, self.recv_ip): 
          return True #ack이 ETTTP 형식이 맞다면 return true
        

        if not check_msg(ack, self.recv_ip):
          return False #아니라면 return False

        ######################################################  

    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################

        if not get: #get이 false인 경우 it means this user is winner
            winner_report = "RESULT ETTTP/1.0\\r\\nHost:" + self.send_ip + "\\r\\nWinner:" + winner + "\\r\\n" #winner_report winner:me 메시지 작성
            self.socket.send(winner_report.encode()) #메시지 전송

            peer_result_msg = self.socket.recv(1024).decode() #패배한 상대로부터 winner:you 메시지 수신
            peer_result_msg = peer_result_msg.replace("\\r\\n","\r\n") #"\\r\\n" 를 "\r\n"으로 대체

            if check_msg(peer_result_msg, self.recv_ip): #ETTTP형식이 맞는지, 올바른 IP주소 인지 먼저 확인하고 맞으면 결과가 맞는 지 확인
                peer_result_msg = peer_result_msg.replace("\r\n", " ") #"\r\n" 를 공백으로 대체
                peer_result_msg = peer_result_msg.replace(":", " ") #":" 를 공백으로 대체
                peer_result_msg = peer_result_msg.split(" ") #공백을 기준으로 split
                peer_result = peer_result_msg[5] #패배한 상대로부터 받은 메시지에서 winner 추출("YOU")

                if peer_result == "YOU": #상대방의 메시지와 결과가 같다면 return True
                    return True 
                else: #결과가 다르다면 return False
                    return False
                
            else: #ETTTP형식이 맞는지, 올바른 IP주소 인지 확인하여 맞지 않으면 False 반환
                return False
            
        else: #get이 True 인 경우
            peer_result_msg = self.socket.recv(1024).decode() #winner_report(winner:me) 메시지를 받음
            peer_result_msg = peer_result_msg.replace("\\r\\n","\r\n") #"\\r\\n" 를 "\r\n"으로 대체

            if check_msg(peer_result_msg, self.recv_ip): #ETTTP형식이 맞는지, 올바른 IP주소 인지 먼저 확인하고 맞으면 결과가 맞는 지 확인
                peer_result_msg = peer_result_msg.replace("\r\n", " ") #"\r\n" 를 공백으로 대체
                peer_result_msg = peer_result_msg.replace(":", " ") #":" 를 공백으로 대체
                peer_result_msg = peer_result_msg.split(" ") #공백을 기준으로 split
                peer_result = peer_result_msg[5] #우승한 상대로부터 받은 메시지에서 winner 추출("ME")

                if peer_result == "ME": #상대방의 메시지와 결과가 같다면
                        ack = "RESULT ETTTP/1.0\\r\\nHost:" + self.send_ip + "\\r\\nWinner:" + winner + "\\r\\n" #winner:you 라는 ack을 작성
                        self.socket.send(ack.encode()) #메시지 전송
                        return True # True 반환
                else: #결과가 같지 않다면 return false
                  return False
                
            else: #ETTTP형식이 맞는지, 올바른 IP주소 인지 확인하여 맞지 않으면 False 반환
                return False
           

        ######################################################
      

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################

    msg = msg.replace("\r\n", " ") #"\r\n"를 공백으로 대체
    msg = msg.replace(":", " ") #":"를 공백으로 대체
    
    lines = msg.split(" ") #공백을 기준으로 문자열 split해서 리스트에 저장

    version = lines[1] #통신 프로토콜과 버전 추출
    ip_line = lines[3] #IP주소 추출


    if version == 'ETTTP/1.0' and ip_line == recv_ip: #ETTTP/1.0 형식에 맞게 보냈는지 아이피 주소가 내 주소가 맞는지 확인
        return True #맞다면 True
    else: #맞지 않다면
        return False #false 리턴

    ######################################################  
