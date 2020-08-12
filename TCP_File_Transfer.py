"""
File name:  TCP_File_Transfer.py
Description:  Main source code for Wireless TCP Socket File Transfer
OS:  Windows or Linux
Author:  Tejas Anilkumar P.  <tpandara@andrew.cmu.edu>
Date:  08/10/2020
   
Carnegie Mellon University
"""

from TCP_helper import *

initTCP()

try:
  fileTransferOption()
  
except KeyboardInterrupt:
    shutdownTCP()
    
    
