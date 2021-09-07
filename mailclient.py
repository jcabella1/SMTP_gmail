# Author: Jay Abella
# Class: CS 441 - Computer Networks
# School: CSU East Bay

# Assignment: Socket Programming Lab 3 - SMTP Lab

# Utilizes ssl to send an email through Google's SMTP server
# Modified 4/29 - Added user input so the user can enter their own username/password and receiver's email

import socket
import ssl
import base64
import getpass

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver =  'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((mailserver, 587))
recv = clientSocket.recv(1024)
print (recv)
if recv[:3] != '220':
    print ('220 reply not received from server.')

# Send HELO command and print server response.
command ='HELO Alice\r\n'
heloCommand = command.encode()
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print ("HELO response: " + recv1.decode())
if recv1[:3] != '250':
    print ('250 reply not received from server.')

#Request an encrypted connection

command = 'STARTTLS\r\n'.encode()
clientSocket.send(command)
recv2 = clientSocket.recv(1024).decode()
print("STARTTLS response: " + recv2)
if recv2[:3] != '220':
    print ('220 reply not received from server')

#Encrypt the socket
clientSocket = ssl.wrap_socket(clientSocket)

#Authentication
sender = input("Enter Sender's Gmail Address: ")
email = (base64.b64encode((sender).encode())+ ('\r\n').encode())
password = (base64.b64encode(getpass.getpass().encode())+ ('\r\n').encode())

# Send AUTH LOGIN command and print server response
clientSocket.send('AUTH LOGIN \r\n'.encode())
recv3 = clientSocket.recv(1024).decode()
print("AUTH LOGIN response: " + recv3)
if recv3[:3] != '334':
    print ('334 reply not received from server')

# Send encrypted email
clientSocket.send(email)
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '334':
    print ('334 reply not received from server')

# Send encrypted password
clientSocket.send(password)
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '235':
    print ('235 reply not received from server')


# Send MAIL FROM command and print server response.
clientSocket.send(("MAIL FROM: <" + sender + ">\r\n").encode())

recv6 = clientSocket.recv(1024).decode()
print("MAIL FROML response: " + recv6)
if recv6[:3] != '250':
    print ('250 reply not received from server.')

# Send RCPT TO command and print server response.
receiver = input("Enter Receiver's Gmail Address: ")
clientSocket.send(("RCPT TO: <" + receiver + ">\r\n").encode())

recv7 = clientSocket.recv(1024).decode()
print("RCPT TO response: " + recv7)

# Send DATA command and print server response.
clientSocket.send("DATA\r\n".encode())
recv8 = clientSocket.recv(1024).decode()
print("DATA response: " + recv8)

#Send data
clientSocket.send(("Subject: Socket Programming 3: SMTP Lab \r\n").encode())
clientSocket.send((receiver + "\r\n").encode())
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)

# Send QUIT command and get server response.
clientSocket.send("QUIT\r\n".encode())
recv10 = clientSocket.recv(1024).decode()
print("QUIT response: " + recv10)

#Close connection with client socket
clientSocket.close()
