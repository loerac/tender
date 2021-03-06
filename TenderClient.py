import socket               # Import socket module
import time
import selectors

class TenderClient:
    
    #Constructor
    #Sets up the socket and selector and sends signon message.
    def __init__(self):
        self.sock = socket.socket()         # Create a socket object

        host = '65.28.168.158'     #Router IP
        port = 22850               #Port to be forwarded

        if self.sock.connect_ex((host, port)) != 0: #Can't hit the Forwarding Port
            print('Attempting localmachine')
            host = socket.gethostname() # Assume localmachine
            port = 12345                
            print (self.sock.connect_ex((host,port)))

        signon = str.encode('signon')
        self.sock.send(signon)
        
        self.sel = selectors.DefaultSelector()
        self.sock.setblocking(0)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
    
    #WriteRead
    #A quick write/read when we expect either a quick response from the Server, or we don't need to do
    #anything in the client.
    #THIS IS ONLY USABLE IF WE SET THE SOCKET TO BLOCKING
    def WriteRead(self,msg):
        self.WriteToSock(msg)
        recv_data = self.sock.recv(1024) #Hang up and wait for response
        return recv_data
    
    #WriteToSock
    #Writes a message to the socket.
    #Could perform a read beforehand to make sure server didn't crash on us.
    def WriteToSock(self,msg):
        toSend = str.encode(msg)
        self.sock.send(toSend)
    
    #ReadFromSock
    #Should be called often after the client sends a message.
    #Checks the read event, and if there is something, returns the message from the Server.
    def ReadFromSock(self):
        events = self.sel.select(timeout=0.1)
        for key,mask in events:
            sock = key.fileobj
            data = key.data
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    return recv_data.decode()
                else:
                    return 'quit'
    
    #CloseConn
    #Close the Connection
    def CloseConn(self):
        
        self.sock.close()
        self.sel.close()