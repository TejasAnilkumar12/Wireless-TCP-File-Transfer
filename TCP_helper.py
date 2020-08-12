"""
File name:  TCP_helper.py
Description:  Helper source code for Wireless TCP Socket File Transfer
OS:  Windows or Linux
Author:  Tejas Anilkumar P.  <tpandara@andrew.cmu.edu>
Date:  08/10/2020
   
Carnegie Mellon University
"""

import os
import socket
import argparse
import sys
import platform
import tqdm
from time import *

def initParser():
    global args,fd_flag,no_file
    fd_flag = False
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode",required=True,help="MODE: Server or Client")
    parser.add_argument("-ip","--server_ip",required=True,help="SERVER_IP: e.g. 192.168.1.10")
    parser.add_argument("-p","--port",default = 5050,help="PORT: e.g. 5050")
    parser.add_argument("-f","--file_location" , help =r"FILE_LOCATION: e.g. Linux: /home/user/filename.extension or Windows: C:\Users\Desktop\filename.extension")
    args = parser.parse_args()
    

def variablesInit():
    global SERVER_HOST,SERVER_PORT,BUFFER_SIZE,SEPARATOR
    SERVER_HOST = args.server_ip
    SERVER_PORT = int(args.port)
    BUFFER_SIZE = 4096
    SEPARATOR = "-"
    

def initTCP():
    initParser()
    variablesInit()
    global sock,client
    try:
        print("Creating Socket\n")
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    except socket.error as err:
        print("Creating Socket Failed\n")
        print(err)
        sock.close()
            
    print("Socket Created\n")
    
    if args.mode == "Server" or args.mode == "s":
              
        print("Binding IP Address and Port\n")
        sock.bind((SERVER_HOST,SERVER_PORT))

        print("Server running at %s:%s\n"%(SERVER_HOST,SERVER_PORT))

        print("Waiting for Client")

        sock.listen()
        client,address = sock.accept()
        print("Client Connected %s:%s"%address)

        
    elif args.mode == "Client" or args.mode == "c":
        print("Connecting to Server %s:%s\n"%(SERVER_HOST,SERVER_PORT))
        
        result = sock.connect_ex((SERVER_HOST,SERVER_PORT))
        #print(result)
        if(result==0):
            print("Connected\n")
            
        else:
            print("Connecting Failed")
            sock.close()
            sys.exit('\nShutting Down')
        
        
    
def clearScreen():
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    elif system == "Linux":
        os.system('clear')


def fileTransferOption():
    n = 0
    if(args.mode == "Server"):
        Socket = client
    else:
        Socket = sock
    while n!= 3:
        n = int(input("Select Option:\n 1. Send Files \n 2. Receive Files\n 3. Exit\n Enter your choice: "))
        clearScreen()
        #print("User input:" +str(n))
        if(n == 1):
            fileTransfer(True,Socket)
        elif(n == 2):
            fileTransfer(False,Socket)
    shutdownTCP()
    
        


def fileTransfer(Mode,Socket):
    
    if(Mode):
        print("Send Mode\n")
        if(args.file_location == None):
            file_loc = str(input("Enter File Location: "))
            if(os.path.isfile(file_loc)):
                sendFile(Socket,file_loc)
            else:
                sys.exit("File not found/Invalid filename")
                
        else:
            if(os.path.isfile(args.file_location)):
                sendFile(Socket,args.file_location)
            else:
                sys.exit("File not found/Invalid filename")
                
            
    else:
        print("Receive Mode\n")
            
        start = Socket.recv(1).decode()
        
        if(start=="s"):
            print("Starting File Receive\n")
            received = Socket.recv(BUFFER_SIZE).decode()
            fileName, fileSize = received.split(SEPARATOR)
            fileName = os.path.basename(fileName)
            fileSize = int(fileSize)
                
            progress = tqdm.tqdm(range(fileSize), f"\nReceiving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(fileName, "wb") as f:
                for i in progress:
                    bytes_read = Socket.recv(BUFFER_SIZE)
                    #print(bytes_read)
                    if bytes_read[-3:] == b'EOP':
                        print("\nReceived End Character")
                        f.write(bytes_read[:-3])
                        break
                 

                    f.write(bytes_read)
                    progress.update(len(bytes_read))
                    
            
                    
        
    
def sendFile(Socket,File):
    Socket.send("s".encode())
    print("Sending Start Character")
    fileName = os.path.split(File)[1]
    fileSize = os.path.getsize(File)
    Socket.send(f"{fileName}{SEPARATOR}{fileSize}".encode())
    # start sending the file
    progress = tqdm.tqdm(range(fileSize), f"\nSending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(File, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
            #File Transfer Done
                break
            Socket.send(bytes_read)
            progress.update(len(bytes_read))
    Socket.send("EOP".encode())
   
    


    

            
def shutdownTCP():
    sock.close()
    if(args.mode == "Server"):
        client.close()
    sys.exit('\nShutting Down')

